from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Lesson, Question, Choice, Enrollment, Submission

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        # Lấy danh sách ID các lựa chọn từ form nộp về
        choices_ids = [value for key, value in request.POST.items() if 'choice_' in key]
        
        # Lấy thông tin đăng ký của user hiện tại
        enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
        
        # Tạo mới một bản ghi Submission
        submission = Submission.objects.create(enrollment=enrollment)
        for choice_id in choices_ids:
            choice = Choice.objects.get(pk=choice_id)
            submission.choices.add(choice)
        submission.save()
        
        # Chuyển hướng sang trang hiển thị kết quả
        return HttpResponseRedirect(reverse('onlinecourse:show_exam_result', args=(course.id, submission.id)))

def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Logic tính điểm (Phần này AI chấm bài yêu cầu rất kỹ)
    total_score = 0
    # Lấy danh sách ID các câu trả lời mà người dùng đã chọn trong submission này
    selected_ids = [choice.id for choice in submission.choices.all()]
    
    # Duyệt qua từng bài học và câu hỏi để tính tổng điểm
    for lesson in course.lesson_set.all():
        for question in lesson.question_set.all():
            # Sử dụng phương thức is_get_score đã định nghĩa trong models.py
            if question.is_get_score(selected_ids):
                total_score += question.grade
                
    # Gán các giá trị vào context để render ra template
    context['course'] = course
    context['submission'] = submission
    context['total_score'] = total_score
    context['selected_ids'] = selected_ids
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)

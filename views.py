def submit(request, course_id):
    course = get_object_ some_model_or_404(Course, pk=course_id)
    if request.method == 'POST':
        choices_ids = [value for key, value in request.POST.items() if 'choice_' in key]
        registration = Enrollment.objects.get(user=request.user, course=course)
        submission = Submission.objects.create(enrollment=registration)
        for choice_id in choices_ids:
            choice = Choice.objects.get(pk=choice_id)
            submission.choices.add(choice)
        submission.save()
        return HttpResponseRedirect(reverse('onlinecourse:show_exam_result', args=(course.id, submission.id)))

def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    context['course'] = course
    context['submission'] = submission
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)

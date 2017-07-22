from django.shortcuts import render


def presentation(request):
    return render(request, 'ctf_board/presentation.html')

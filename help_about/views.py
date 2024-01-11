from django.http import HttpResponse, JsonResponse
from django.http import FileResponse
import base64
import os

def get_help(request):
    pdf_path = 'static/Help/help.pdf'

    if os.path.exists(pdf_path):
        try:
            with open(pdf_path, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'inline; filename="help.pdf"'
                return response
        except Exception as e:
            return HttpResponse("Error reading PDF file", status=500)
    else:
        return HttpResponse("PDF file not found", status=404)

def get_image_base64(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return f'data:image/jpg;base64,{encoded_image}'

def about_us(request):
    developers = [
        {
            'name' : 'Yash Raj Pandeya',
            'role' : 'Project Manager',
            'gmail' : 'www.gmail.com',
            'linkedin' : 'www.linkedin.com',
            'facebook' : 'www.facebook.com',
            'github' : '',

            'image_url': '/static/Developers/Yash_Pandeya.jpg',
            'details': "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five",
        },
        {
            'name' : 'Prajwal THapa',
            'role' : 'Full Stack Developer',
            'gmail' : 'prazzwalthapa87@gmail.com',
            'linkedin' : 'https://www.linkedin.com/in/prajwal-thapa-64048a1a4/',
            'facebook' : 'https://www.facebook.com/prazwal.j.thapa',
            'github' : 'https://github.com/Prajwal247',
            'image_url': '/static/Developers/prajwal_thapa.png',
            'details': "As an AI student and full-stack developer, I blend my academic insights in artificial intelligence with hands-on experience in building end-to-end web applications. My focus on deep learning reflects a profound interest in harnessing neural networks to solve intricate problems. With a versatile skill set covering both frontend and backend technologies, I aspire to contribute to projects that seamlessly integrate AI innovations into real-world applications, delivering both technical excellence and user-centric solutions.",
        },
        {
            'name' : 'Safal Shrestha',
            'role' : 'Full Stack Developer',
            'gmail' : 'dev.safalstha@gmail.com',
            'linkedin' : 'https://www.linkedin.com/in/itsmesafal/',
            'facebook' : 'https://www.facebook.com/sth1111a/',
            'github' : 'https://github.com/whoamisafal',
            'image_url': '/static/Developers/safal_shrestha.png',
            'details': "Hello! I am an Android full-stack developer and a passionate AI enthusiast currently pursuing my studies at Kathmandu University. With a keen interest in creating seamless mobile experiences, I specialize in building robust and user-friendly Android applications. My journey extends beyond mobile development, delving into the exciting realm of artificial intelligence. Through my academic pursuits, I am dedicated to merging the worlds of cutting-edge technology and practical development, constantly seeking opportunities to innovate and create impactful solutions.",
        },
               {
            'name' : 'Nimesh Timalsina',
            'role' : 'Designer',
            'gmail' : 'nimeshtimalsina@gmail.com',
            'linkedin' : 'https://www.linkedin.com/in/nimesh-timalsina-2495b8266/',
            'facebook' : 'https://www.facebook.com/nimesh.timalsina.90',
            'github' : 'https://github.com/GOGHSY',
            'image_url': '/static/Developers/nimeshimage.jpg',
            'details': "Designer with a passion for AI, blending creativity with technology to craft innovative and user-centric experiences. Excited about pushing the boundaries of design through the possibilities offered by artificial intelligence.",
        },
         
    ]

    return JsonResponse({'developers': developers})
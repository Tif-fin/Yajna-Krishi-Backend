from django.http import HttpResponse, JsonResponse
from django.http import FileResponse
import base64
import os


def get_help(request):
    pdf_path = "static/Help/help.pdf"

    if os.path.exists(pdf_path):
        try:
            with open(pdf_path, "rb") as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type="application/pdf")
                response["Content-Disposition"] = 'inline; filename="help.pdf"'
                return response
        except Exception as e:
            return HttpResponse("Error reading PDF file", status=500)
    else:
        return HttpResponse("PDF file not found", status=404)


def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:image/jpg;base64,{encoded_image}"


def about_us(request):
    developers = [
        {
            "name": "Dr. Yash Raj Pandeya",
            "role": "Principal Investigator (PI)",
            "gmail": "yagya.pandeya@ku.edu.np",
            "linkedin": "https://www.linkedin.com/in/yagya-raj-pandey-13377a68/",
            "facebook": "https://www.facebook.com/yagya.pandeya",
            "github": "https://yagyapandeya.github.io/",
            "image_url": "/static/Developers/Yash_Pandeya.jpg",
            "details": "I am an assistant professor in Computer science and Engineeing department at Kathmandu University, and also affiliated to the Jeonbuk National University, Fuse machine Nepal, and Guru technology research group in Nepal. I have a good experience of deep learning and machine learning technologies for image, audio, music, video and text processing using supervised and unsupervised classification, multi-level classification, self-supervised learning, meta-learning, incremental learning and generative networks (GAN, VAE), which are some of my major interest areas.",
        },
        {
            "name": "Dr. Kumar Lama",
            "role": "Assistant Professor and AG program Coordinator (Co PI)",
            "gmail": "https://scholar.google.com/citations?hl=en&amp;user=TUteV2MAAAAJ",
            "linkedin": "https://www.linkedin.com/in/kumar-lama-phd-41749161/",
            "facebook": "https://www.facebook.com/kumar.lama.98478",
            "github": "",
            "image_url": "/static/Developers/Kumar_lama.jpg",
            "details": "",
        },
        {
            "name": "Roshan Subedi",
            "role": "Lecturer (Co PI)",
            "gmail": "yagya.pandeya@ku.edu.np",
            "linkedin": "https://www.linkedin.com/in/roshan-subedi-8259365b/",
            "facebook": "https://www.facebook.com/roshan.subedi.526",
            "github": "",
            "image_url": "/static/Developers/roshan.jpg",
            "details": "",
        },
        {
            "name": "Harish Chandra Bhandari",
            "role": "Lecturer (Co PI)",
            "gmail": "",
            "linkedin": "https://www.linkedin.com/in/harish-chandra-bhandari-6a714427b/?fbclid=IwAR37Murk-L6XTDCy3WEEt835spQJJR7boptKF5_DoTHcKkWKya4Q311OjhE",
            "facebook": "https://www.linkedin.com/in/kumar-lama-phd-41749161/",
            "github": "",
            "image_url": "/static/Developers/Harish_Pic.jpg",
            "details": "",
        },
        {
            "name": "Rojina Shakya",
            "role": "Lecturer (Co PI)",
            "gmail": "",
            "linkedin": "https://www.linkedin.com/in/rojina-shakya-3b3651a6/",
            "facebook": "https://www.facebook.com/rojina.shakya29",
            "github": "",
            "image_url": "/static/Developers/Rojina_Shakya.JPG",
            "details": "",
        },
        {
            "name": "Prajwal Thapa",
            "role": "Full Stack Developer",
            "gmail": "prazzwalthapa87@gmail.com",
            "linkedin": "https://www.linkedin.com/in/prajwal-thapa-64048a1a4/",
            "facebook": "https://www.facebook.com/prazwal.j.thapa",
            "github": "https://github.com/Prajwal247",
            "image_url": "/static/Developers/prajwal_thapa.png",
            "details": "As an AI student and full-stack developer, I blend my academic insights in artificial intelligence with hands-on experience in building end-to-end web applications. My focus on deep learning reflects a profound interest in harnessing neural networks to solve intricate problems. With a versatile skill set covering both frontend and backend technologies, I aspire to contribute to projects that seamlessly integrate AI innovations into real-world applications, delivering both technical excellence and user-centric solutions.",
        },
        {
            "name": "Safal Shrestha",
            "role": "Full Stack Developer",
            "gmail": "dev.safalstha@gmail.com",
            "linkedin": "https://www.linkedin.com/in/itsmesafal/",
            "facebook": "https://www.facebook.com/sth1111a/",
            "github": "https://github.com/whoamisafal",
            "image_url": "/static/Developers/safal_shrestha.png",
            "details": "Hello! I am an Android full-stack developer and a passionate AI enthusiast currently pursuing my studies at Kathmandu University. With a keen interest in creating seamless mobile experiences, I specialize in building robust and user-friendly Android applications. My journey extends beyond mobile development, delving into the exciting realm of artificial intelligence. Through my academic pursuits, I am dedicated to merging the worlds of cutting-edge technology and practical development, constantly seeking opportunities to innovate and create impactful solutions.",
        },
        {
            "name": "Nimesh Timalsina",
            "role": "Designer",
            "gmail": "nimeshtimalsina@gmail.com",
            "linkedin": "https://www.linkedin.com/in/nimesh-timalsina-2495b8266/",
            "facebook": "https://www.facebook.com/nimesh.timalsina.90",
            "github": "https://github.com/GOGHSY",
            "image_url": "/static/Developers/nimeshimage.jpg",
            "details": "Designer with a passion for AI, blending creativity with technology to craft innovative and user-centric experiences. Excited about pushing the boundaries of design through the possibilities offered by artificial intelligence.",
        },
        {
            "name": "Baburam Chaudhary",
            "role": "CO PI",
            "gmail": "baburam.ch208@gmail.com",
            "linkedin": "https://www.linkedin.com/in/baburamchaudhary/",
            "facebook": "",
            "github": "",
            "image_url": "/static/Developers/baburam.jpg",
            "details": "Passionate AI student",
        },
    ]

    return JsonResponse({"developers": developers})

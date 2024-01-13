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
            "name": "यज्ञ राज पाण्डेय, पि.एच.डी.",
            "role": "Principal Investigator (PI)",
            "gmail": "yagya.pandeya@ku.edu.np",
            "linkedin": "https://www.linkedin.com/in/yagya-raj-pandey-13377a68/",
            "facebook": "https://www.facebook.com/yagya.pandeya",
            "github": "https://yagyapandeya.github.io/",
            "image_url": "/static/Developers/Yash_Pandeya.jpg",
            "details": "डा यज्ञराज पाण्डेय यो परियोजनामा प्रमुख अनुसन्धानकर्ताको भूमिकामा हुनुहुन्छ, उहाले परियोजना परिकल्पना, योजना निर्माण तथा कार्यान्वयनको सम्पूर्ण काममा सहयोग गर्नुभएको हो।",
        },
        {
            "name": "कुमार लामा, पि.एच.डी.",
            "role": "Assistant Professor and AG program Coordinator (Co PI)",
            "gmail": "https://scholar.google.com/citations?hl=en&amp;user=TUteV2MAAAAJ",
            "linkedin": "https://www.linkedin.com/in/kumar-lama-phd-41749161/",
            "facebook": "https://www.facebook.com/kumar.lama.98478",
            "github": "",
            "image_url": "/static/Developers/Kumar_lama.jpg",
            "details": "डा कुमार लामा यो परियोजनामा सह-अनुसन्धानकर्ताको भूमिकामा हुनुहुन्छ, उहाले परियोजना प्रस्ताव निर्माण, बजेट संकलन तथा समन्वयनको काममा सहयोग गर्नुभएको हो।",
        },
        {
            "name": "रोसन सुवेदी",
            "role": "Lecturer (Co PI)",
            "gmail": "yagya.pandeya@ku.edu.np",
            "linkedin": "https://www.linkedin.com/in/roshan-subedi-8259365b/",
            "facebook": "https://www.facebook.com/roshan.subedi.526",
            "github": "",
            "image_url": "/static/Developers/roshan.jpg",
            "details": "रोसन सुबेदी यो परियोजनामा सह-अनुसन्धानकर्ताको भूमिकामा हुनुहुन्छ, उहाले परियोजना प्रस्ताव निर्माण, मोबाईल एप्प निर्माण र लेखन कार्यमा सहयोग गर्नुभएको हो।",
        },
        {
            "name": "हरिसचन्द्र भणडारी",
            "role": "Lecturer (Co PI)",
            "gmail": "",
            "linkedin": "https://www.linkedin.com/in/harish-chandra-bhandari-6a714427b/?fbclid=IwAR37Murk-L6XTDCy3WEEt835spQJJR7boptKF5_DoTHcKkWKya4Q311OjhE",
            "facebook": "https://www.linkedin.com/in/kumar-lama-phd-41749161/",
            "github": "",
            "image_url": "/static/Developers/Harish_Pic.jpg",
            "details": "हरिसचन्द्र भणडारी यो परियोजनामा सह-अनुसन्धानकर्ताको भूमिकामा हुनुहुन्छ, उहाले परियोजना प्रस्ताव निर्माण, कम्प्युटरको कृत्रिम बुद्धिमत्ता विकास र लेखन कार्यमा सहयोग गर्नुभएको हो।",
        },
        {
            "name": "रोजिना शाक्य",
            "role": "Lecturer (Co PI)",
            "gmail": "",
            "linkedin": "https://www.linkedin.com/in/rojina-shakya-3b3651a6/",
            "facebook": "https://www.facebook.com/rojina.shakya29",
            "github": "",
            "image_url": "/static/Developers/Rojina_Shakya.JPG",
            "details": "रोजिना शाक्य यो परियोजनामा सह-अनुसन्धानकर्ताको भूमिकामा हुनुहुन्छ, उहाले परियोजनाको आर्थिक बिबरण र समन्वयनको काममा सहयोग गर्नुभएको हो।",
        },
        {
            "name": "प्रज्वल थापा",
            "role": "Full Stack Developer",
            "gmail": "prazzwalthapa87@gmail.com",
            "linkedin": "https://www.linkedin.com/in/prajwal-thapa-64048a1a4/",
            "facebook": "https://www.facebook.com/prazwal.j.thapa",
            "github": "https://github.com/Prajwal247",
            "image_url": "/static/Developers/prajwal_thapa.png",
            "details": "प्रज्वल थापा यो परियोजनामा अनुसन्धान-सहयोगीको भूमिकामा हुनुहुन्छ, उहाले परियोजनामा मोबाईल एप्प निर्माण र लेखन कार्यमा सहयोग गर्नुभएको हो।",
        },
        {
            "name": "सफल श्रेष्ठ",
            "role": "Full Stack Developer",
            "gmail": "dev.safalstha@gmail.com",
            "linkedin": "https://www.linkedin.com/in/itsmesafal/",
            "facebook": "https://www.facebook.com/sth1111a/",
            "github": "https://github.com/whoamisafal",
            "image_url": "/static/Developers/safal_shrestha.png",
            "details": "सफल श्रेष्ठ यो परियोजनामा अनुसन्धान-सहयोगीको भूमिकामा हुनुहुन्छ, उहाले परियोजनामा मोबाईल एप्प निर्माण कार्यमा सहयोग गर्नुभएको हो।",
        },
        {
            "name": "निमेष तिमल्सिना",
            "role": "Designer",
            "gmail": "nimeshtimalsina@gmail.com",
            "linkedin": "https://www.linkedin.com/in/nimesh-timalsina-2495b8266/",
            "facebook": "https://www.facebook.com/nimesh.timalsina.90",
            "github": "https://github.com/GOGHSY",
            "image_url": "/static/Developers/nimeshimage.jpg",
            "details": "निमेष तिमल्सिना यो परियोजनामा अनुसन्धान-सहयोगीको भूमिकामा हुनुहुन्छ, उहाले परियोजनामा ग्राफिक्स डिजाइन कार्यमा सहयोग गर्नुभएको हो।",
        },
        {
            "name": "बाबुराम चौधरी",
            "role": "CO PI",
            "gmail": "baburam.ch208@gmail.com",
            "linkedin": "https://www.linkedin.com/in/baburamchaudhary/",
            "facebook": "",
            "github": "",
            "image_url": "/static/Developers/baburam.jpg",
            "details": "बाबुराम चौधरी यो परियोजनामा अनुसन्धान-सहयोगीको भूमिकामा हुनुहुन्छ, उहाले परियोजनामा कम्प्युटरको कृत्रिम बुद्धिमत्ता विकास र लेखन कार्यमा सहयोग गर्नुभएको हो।",
        },
    ]

    return JsonResponse({"developers": developers})

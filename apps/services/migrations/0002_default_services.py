from django.db import migrations


SERVICES = [
    {
        "title": "Website Development",
        "slug": "website-development",
        "category": "website",
        "short_description": "Responsive, high-performance websites and custom applications tailored to your business.",
        "description": "Build a professional online presence with responsive, high-performance and custom-developed websites. We plan around your audience and business goals, then create a maintainable experience that works across devices.",
        "benefits": "Clear and accessible customer experience\nResponsive on desktop, tablet and mobile\nMaintainable foundation for future growth",
        "features": "Business and corporate websites\nPortfolio websites\nCustom web applications\nResponsive web design\nContent management integration",
        "technologies": "Django, Python, HTML, CSS, JavaScript",
        "icon": "fa-code",
        "display_order": 1,
    },
    {
        "title": "E-Commerce Development",
        "slug": "ecommerce-development",
        "category": "ecommerce",
        "short_description": "Secure, scalable and user-friendly online stores built for a smooth shopping journey.",
        "description": "Launch your online business with a thoughtfully structured e-commerce platform. We focus on product discovery, a clear shopping flow and the practical tools needed to manage orders.",
        "benefits": "Straightforward product discovery\nA consistent shopping experience across devices\nPractical order and catalogue workflows",
        "features": "Online store development\nProduct management\nShopping cart\nPayment gateway integration\nOrder management",
        "technologies": "Django, Python, HTML, CSS, JavaScript",
        "icon": "fa-cart-shopping",
        "display_order": 2,
    },
    {
        "title": "Cloud Services",
        "slug": "cloud-services",
        "category": "cloud",
        "short_description": "Reliable cloud infrastructure, application hosting and deployment solutions.",
        "description": "Deploy and manage modern applications with reliable cloud infrastructure and deployment solutions. We help plan an appropriate environment, configure services and prepare a repeatable launch process.",
        "benefits": "A deployment approach matched to your application\nMore consistent releases\nInfrastructure that can adapt as needs change",
        "features": "Cloud deployment\nServer configuration\nApplication hosting\nInfrastructure management\nCI/CD implementation",
        "technologies": "Linux, cloud hosting platforms, Docker, CI/CD tooling",
        "icon": "fa-cloud",
        "display_order": 3,
    },
]


def create_services(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    for item in SERVICES:
        Service.objects.get_or_create(category=item["category"], defaults=item)


def remove_services(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    Service.objects.filter(slug__in=[item["slug"] for item in SERVICES]).delete()


class Migration(migrations.Migration):
    dependencies = [("services", "0001_initial")]

    operations = [migrations.RunPython(create_services, remove_services)]

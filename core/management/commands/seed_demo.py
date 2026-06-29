"""
Management command to seed the database with demo data.
Run: python manage.py seed_demo
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from core.models import (
    User, ConsultantProfile,
    LifePlan, NonLifePlan,
)


class Command(BaseCommand):
    help = 'Seed the database with demo consultants and plans'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding demo data...')

        # Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@insurelink.com', 'admin1234', role='member')
            self.stdout.write('  ✅ Superuser: admin / admin1234')

        # ── Consultant 1 ────────────────────────────────────
        u1, _ = User.objects.get_or_create(
            username='sentinel_ins',
            defaults={
                'first_name': 'Maria', 'last_name': 'Santos',
                'email': 'maria@sentinel.com', 'role': 'consultant', 'phone': '+63 917 555 0001',
            }
        )
        u1.set_password('pass1234')
        u1.save()

        c1, _ = ConsultantProfile.objects.get_or_create(
            user=u1,
            defaults={
                'company_name': 'Sentinel Insurance Corp.',
                'license_number': 'IC-2019-00142',
                'bio': 'Trusted provider of life and motor insurance since 2005. We believe in building lasting protection for Filipino families.',
                'years_experience': 18,
                'specialization': 'Life & Motor Insurance',
            }
        )

        # Life Plans for C1
        LifePlan.objects.get_or_create(
            consultant=c1, name='Family Shield Term Plan',
            defaults={
                'plan_type': 'term', 'description': 'Affordable term life coverage for the whole family.',
                'coverage_amount_min': 500000, 'coverage_amount_max': 5000000,
                'premium_from': 1200, 'premium_period': 'monthly',
                'age_min': 18, 'age_max': 60, 'term_years': 20,
            }
        )
        LifePlan.objects.get_or_create(
            consultant=c1, name='Whole Life Secure Plan',
            defaults={
                'plan_type': 'whole', 'description': 'Lifelong protection with cash value build-up.',
                'coverage_amount_min': 1000000, 'coverage_amount_max': 10000000,
                'premium_from': 3500, 'premium_period': 'monthly',
                'age_min': 21, 'age_max': 55,
            }
        )

        # Non-Life Plans for C1
        NonLifePlan.objects.get_or_create(
            consultant=c1, name='AutoGuard Comprehensive',
            defaults={
                'category': 'motor',
                'description': 'Full protection for your vehicle against loss, theft, and third-party liability.',
                'coverage_details': 'Own damage, theft, Acts of God, 3rd party liability (CTPL included)',
                'exclusions': 'Racing, deliberate damage, wear and tear',
                'premium_from': 8000, 'premium_period': 'annual',
            }
        )
        NonLifePlan.objects.get_or_create(
            consultant=c1, name='HomeGuard Fire & Allied Perils',
            defaults={
                'category': 'property',
                'description': 'Protect your home and belongings from fire, flood, and natural calamities.',
                'coverage_details': 'Fire, lightning, typhoon, flood, earthquake, theft',
                'exclusions': 'War, nuclear risks, intentional acts',
                'premium_from': 3500, 'premium_period': 'annual',
            }
        )

        self.stdout.write(f'  ✅ Consultant 1: sentinel_ins / pass1234 ({c1.company_name})')

        # ── Consultant 2 ────────────────────────────────────
        u2, _ = User.objects.get_or_create(
            username='pinnacle_assure',
            defaults={
                'first_name': 'Jose', 'last_name': 'Reyes',
                'email': 'jose@pinnacle.com', 'role': 'consultant', 'phone': '+63 918 555 0002',
            }
        )
        u2.set_password('pass1234')
        u2.save()

        c2, _ = ConsultantProfile.objects.get_or_create(
            user=u2,
            defaults={
                'company_name': 'Pinnacle Assurance Group',
                'license_number': 'IC-2021-00389',
                'bio': 'Specialists in health, travel, and business insurance for modern Filipinos.',
                'years_experience': 9,
                'specialization': 'Health & Business Insurance',
            }
        )

        LifePlan.objects.get_or_create(
            consultant=c2, name='EndowPro Savings Plan',
            defaults={
                'plan_type': 'endowment',
                'description': 'Dual-purpose plan that combines life protection with guaranteed savings.',
                'coverage_amount_min': 200000, 'coverage_amount_max': 2000000,
                'premium_from': 2800, 'premium_period': 'monthly',
                'age_min': 18, 'age_max': 50, 'term_years': 10,
            }
        )
        NonLifePlan.objects.get_or_create(
            consultant=c2, name='MedShield Health Plan',
            defaults={
                'category': 'health',
                'description': 'Comprehensive health coverage for individuals and families.',
                'coverage_details': 'Hospitalization, surgery, outpatient consults, diagnostics, medicines',
                'exclusions': 'Pre-existing conditions (first year), cosmetic procedures',
                'premium_from': 6500, 'premium_period': 'annual',
            }
        )
        NonLifePlan.objects.get_or_create(
            consultant=c2, name='TravelSafe Worldwide',
            defaults={
                'category': 'travel',
                'description': 'Travel with confidence. Covers medical emergencies, trip cancellations, and lost baggage worldwide.',
                'coverage_details': 'Medical emergency, evacuation, trip cancellation, baggage loss, flight delay',
                'exclusions': 'Pre-existing conditions, high-risk activities without rider',
                'premium_from': 850, 'premium_period': 'per trip',
            }
        )
        NonLifePlan.objects.get_or_create(
            consultant=c2, name='BizCover Commercial Package',
            defaults={
                'category': 'business',
                'description': 'All-in-one commercial insurance for SMEs and enterprises.',
                'coverage_details': 'Property, fire, liability, business interruption, employee benefits',
                'exclusions': 'Cyber risks (available as add-on), illegal operations',
                'premium_from': 25000, 'premium_period': 'annual',
            }
        )

        self.stdout.write(f'  ✅ Consultant 2: pinnacle_assure / pass1234 ({c2.company_name})')

        # ── Demo Member ──────────────────────────────────────
        m1, _ = User.objects.get_or_create(
            username='demo_member',
            defaults={
                'first_name': 'Ana', 'last_name': 'Cruz',
                'email': 'ana@example.com', 'role': 'member', 'phone': '+63 916 555 9999',
            }
        )
        m1.set_password('pass1234')
        m1.save()
        self.stdout.write('  ✅ Demo member: demo_member / pass1234')

        self.stdout.write(self.style.SUCCESS('\n🎉 Demo data seeded successfully!'))
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('  Admin:       admin / admin1234  →  /admin/')
        self.stdout.write('  Consultant1: sentinel_ins / pass1234')
        self.stdout.write('  Consultant2: pinnacle_assure / pass1234')
        self.stdout.write('  Member:      demo_member / pass1234')

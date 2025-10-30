from django.shortcuts import get_object_or_404
from ..models import CaregiverMaster, CaregiverReview , CaregiverDetail
from django.db.models import Avg

def get_all_caregivers():
    """Returns a queryset of all caregivers."""
    return CaregiverMaster.objects.all()

def get_caregiver_by_id(caregiver_id):
    """Returns a single caregiver object by ID. Raises 404 if not found."""
    return get_object_or_404(CaregiverMaster, pk=caregiver_id)

def get_caregiver_dynamic_fields(caregiver):
    """
    Returns a list of (field_verbose_name, value) tuples for a caregiver,
    excluding manually displayed fields.
    """
    excluded = [
        'caregiver_id', 'full_name', 'profile_photo', 
        'start_hourly_rate', 'end_hourly_rate', 'check_status'
    ]
    
    return [
        (f.verbose_name.title(), getattr(caregiver, f.name))
        for f in caregiver._meta.get_fields()
        if f.concrete and f.name not in excluded
    ]

# --- New Functions for Reviews ---
def get_reviews_for_caregiver(caregiver_id):
    """
    Returns a queryset of reviews for a given caregiver ID, newest first.
    """
    return CaregiverReview.objects.filter(caregiver_id=caregiver_id).order_by('-review_id')

# def get_average_rating_for_caregiver(caregiver_id):
#     """
#     Returns the average rating for a caregiver. Returns None if no reviews exist.
#     """
#     result = CaregiverReview.objects.filter(caregiver_id=caregiver_id).aggregate(avg_rating=Avg('rating'))
#     return result['avg_rating']

def get_average_rating_for_caregiver(caregiver_id):
    """
    Returns the average rating for a caregiver. Returns 0 if no reviews exist.
    """
    result = CaregiverReview.objects.filter(caregiver_id=caregiver_id).aggregate(avg_rating=Avg('rating'))
    avg = result['avg_rating']
    return round(avg, 1) if avg else 0

def get_caregiver_with_reviews(caregiver_id):
    """
    Returns a dictionary containing caregiver object, its reviews, and average rating.
    """
    caregiver = get_caregiver_by_id(caregiver_id)
    reviews = get_reviews_for_caregiver(caregiver_id)
    avg_rating = get_average_rating_for_caregiver(caregiver_id)
    return {
        'caregiver': caregiver,
        'reviews': reviews,
        'average_rating': avg_rating
    }

# --- New Functions for Details ---

def get_caregiver_detail_by_id(caregiver_id):
    """
    Returns the CaregiverDetail object for a given caregiver_id.
    Raises 404 if not found.
    """
    return get_object_or_404(CaregiverDetail, caregiver_id=caregiver_id)


def get_caregiver_highlights_and_functionality(caregiver_id):
    """
    Returns a dictionary with 'highlights' and 'functionality' for a given caregiver.
    """
    caregiver_detail = get_caregiver_detail_by_id(caregiver_id)
    return {
        'highlights': caregiver_detail.highlights,
        'functionality': caregiver_detail.functionality
    }


def get_caregiver_dynamic_details(caregiver_id):
    """
    Returns highlights and functionality as lists (split by newline) for easier display.
    """
    caregiver_detail = get_caregiver_detail_by_id(caregiver_id)
    return {
        'highlights': caregiver_detail.highlights.split("\n"),
        'functionality': caregiver_detail.functionality.split("\n")
    }


def get_caregiver_full_profile(caregiver_id):
    """
    Returns a dictionary containing caregiver's profile and detail information.
    """
    caregiver_master = get_caregiver_by_id(caregiver_id)
    caregiver_detail = get_caregiver_highlights_and_functionality(caregiver_id)

    return {
        'caregiver_profile': {
            'full_name': caregiver_master.full_name,
            'dob': caregiver_master.dob,
            'gender': caregiver_master.gender,
            'language': caregiver_master.language,
            'start_hourly_rate': caregiver_master.start_hourly_rate,
            'end_hourly_rate': caregiver_master.end_hourly_rate,
            'check_status': caregiver_master.check_status,
        },
        'caregiver_details': caregiver_detail
    }

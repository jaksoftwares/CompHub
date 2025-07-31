#accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinLengthValidator
from django.utils import timezone
from PIL import Image
import uuid
import os


def user_profile_image_path(instance, filename):
    """Generate file path for user profile images"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('profile_images', str(instance.user.id), filename)


def verification_document_path(instance, filename):
    """Generate file path for verification documents"""
    ext = filename.split('.')[-1]
    filename = f'verification_{uuid.uuid4()}.{ext}'
    return os.path.join('verification_docs', str(instance.user.id), filename)


class User(AbstractUser):
    """
    Extended User model for Dovepeak CompHub
    Supports Buyers, Vendors, and Admins
    """
    USER_TYPE_CHOICES = [
        ('buyer', 'Buyer'),
        ('vendor', 'Vendor'),
        ('admin', 'Admin'),
    ]
    
    VERIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
    ]
    
    # Basic Information
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='buyer')
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?254[0-9]{9}$', message='Enter valid Kenyan phone number')],
        unique=True,
        help_text='Format: +254XXXXXXXXX'
    )
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    
    # Verification and Trust
    verification_status = models.CharField(
        max_length=10, 
        choices=VERIFICATION_STATUS_CHOICES, 
        default='pending'
    )
    verification_date = models.DateTimeField(null=True, blank=True)
    trust_score = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    
    # Activity Tracking
    last_active = models.DateTimeField(auto_now=True)
    is_active_buyer = models.BooleanField(default=True)
    is_active_vendor = models.BooleanField(default=False)
    
    # Privacy and Security
    accept_marketing = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'accounts_user'
        indexes = [
            models.Index(fields=['user_type', 'verification_status']),
            models.Index(fields=['email', 'phone_number']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    def save(self, *args, **kwargs):
        # Set active flags based on user type
        if self.user_type == 'vendor':
            self.is_active_vendor = True
        elif self.user_type == 'buyer':
            self.is_active_buyer = True
        super().save(*args, **kwargs)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def is_verified(self):
        return self.verification_status == 'verified'
    
    @property
    def can_sell(self):
        return self.user_type == 'vendor' and self.is_verified


class UserProfile(models.Model):
    """
    Extended profile information for all users
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal Information
    profile_image = models.ImageField(
        upload_to=user_profile_image_path, 
        null=True, 
        blank=True,
        help_text='Profile picture (max 2MB)'
    )
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Location Information
    county = models.CharField(max_length=50, default='Nairobi')
    sub_county = models.CharField(max_length=50, blank=True)
    ward = models.CharField(max_length=50, blank=True)
    postal_address = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    
    # Preferences
    preferred_language = models.CharField(max_length=10, default='en')
    preferred_currency = models.CharField(max_length=3, default='KES')
    notification_preferences = models.JSONField(default=dict, blank=True)
    
    # Privacy Settings
    profile_visibility = models.CharField(
        max_length=10,
        choices=[('public', 'Public'), ('private', 'Private')],
        default='public'
    )
    show_phone = models.BooleanField(default=False)
    show_email = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'accounts_user_profile'
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize profile image if it exists
        if self.profile_image:
            img = Image.open(self.profile_image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_image.path)


class UserVerification(models.Model):
    """
    KYC verification for users (especially vendors)
    """
    DOCUMENT_TYPE_CHOICES = [
        ('national_id', 'National ID'),
        ('passport', 'Passport'),
        ('business_permit', 'Business Permit'),
        ('kra_pin', 'KRA PIN Certificate'),
        ('bank_statement', 'Bank Statement'),
        ('utility_bill', 'Utility Bill'),
        ('shop_photo', 'Shop Photo'),
        ('other', 'Other Document'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_docs')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    document_file = models.FileField(
        upload_to=verification_document_path,
        help_text='Upload clear photo/scan of document (max 5MB)'
    )
    document_number = models.CharField(max_length=50, blank=True)
    
    # Verification Details
    submitted_at = models.DateTimeField(auto_now_add=True)
    verified_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='verified_documents'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_notes = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    
    # Additional Fields
    expiry_date = models.DateField(null=True, blank=True)
    is_primary = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'accounts_user_verification'
        unique_together = ['user', 'document_type', 'document_number']
        indexes = [
            models.Index(fields=['user', 'is_approved']),
            models.Index(fields=['submitted_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_document_type_display()}"


class VendorProfile(models.Model):
    """
    Extended profile for vendor users
    """
    BUSINESS_TYPE_CHOICES = [
        ('sole_proprietor', 'Sole Proprietor'),
        ('partnership', 'Partnership'),
        ('limited_company', 'Limited Company'),
        ('cooperative', 'Cooperative'),
        ('other', 'Other'),
    ]
    
    SHOP_CATEGORY_CHOICES = [
        ('computers', 'Computers & Laptops'),
        ('mobile', 'Mobile Devices'),
        ('accessories', 'IT Accessories'),
        ('networking', 'Networking Equipment'),
        ('software', 'Software & Licenses'),
        ('repairs', 'Repair Services'),
        ('general', 'General Electronics'),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='vendor_profile',
        limit_choices_to={'user_type': 'vendor'}
    )
    
    # Business Information
    business_name = models.CharField(max_length=200)
    business_registration_number = models.CharField(max_length=50, blank=True)
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPE_CHOICES)
    kra_pin = models.CharField(
        max_length=11,
        validators=[RegexValidator(regex=r'^[AP][0-9]{9}[A-Z]$', message='Enter valid KRA PIN')],
        blank=True
    )
    
    # Shop Details
    shop_name = models.CharField(max_length=200)
    shop_description = models.TextField(max_length=1000)
    shop_category = models.CharField(max_length=20, choices=SHOP_CATEGORY_CHOICES)
    shop_logo = models.ImageField(
        upload_to='shop_logos/', 
        null=True, 
        blank=True,
        help_text='Shop logo (recommended 200x200px)'
    )
    
    # Physical Location
    physical_address = models.TextField(max_length=300)
    building_name = models.CharField(max_length=100, blank=True)
    floor_number = models.CharField(max_length=10, blank=True)
    shop_number = models.CharField(max_length=20, blank=True)
    landmark = models.CharField(max_length=100, blank=True)
    
    # Coordinates for mapping
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    
    # Contact Information
    business_phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?254[0-9]{9}$')]
    )
    business_email = models.EmailField(blank=True)
    whatsapp_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?254[0-9]{9}$')],
        blank=True
    )
    
    # Operating Information
    operating_hours = models.JSONField(
        default=dict,
        help_text='Store opening/closing times for each day'
    )
    delivery_available = models.BooleanField(default=False)
    pickup_available = models.BooleanField(default=True)
    
    # Token System
    token_balance = models.PositiveIntegerField(default=0)
    total_tokens_purchased = models.PositiveIntegerField(default=0)
    total_tokens_used = models.PositiveIntegerField(default=0)
    
    # Performance Metrics
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_orders = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    response_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Status and Settings
    is_featured = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    auto_approve_orders = models.BooleanField(default=False)
    
    # Timestamps
    shop_established_date = models.DateField(null=True, blank=True)
    joined_platform_date = models.DateTimeField(auto_now_add=True)
    last_token_purchase = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'accounts_vendor_profile'
        indexes = [
            models.Index(fields=['shop_category', 'is_featured']),
            models.Index(fields=['average_rating', 'total_orders']),
            models.Index(fields=['token_balance']),
        ]
    
    def __str__(self):
        return f"{self.shop_name} ({self.business_name})"
    
    @property
    def has_sufficient_tokens(self):
        return self.token_balance > 0
    
    @property
    def is_top_rated(self):
        return self.average_rating >= 4.5 and self.total_orders >= 50


class LoginAttempt(models.Model):
    """
    Track login attempts for security monitoring
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email_or_username = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    success = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'accounts_login_attempt'
        indexes = [
            models.Index(fields=['ip_address', 'timestamp']),
            models.Index(fields=['user', 'success']),
        ]
    
    def __str__(self):
        status = "SUCCESS" if self.success else "FAILED"
        return f"{self.email_or_username} - {status} at {self.timestamp}"


class UserActivity(models.Model):
    """
    Track user activity for analytics and security
    """
    ACTIVITY_TYPE_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('profile_update', 'Profile Update'),
        ('password_change', 'Password Change'),
        ('verification_submit', 'Verification Submitted'),
        ('product_view', 'Product Viewed'),
        ('shop_visit', 'Shop Visited'),
        ('search', 'Search Performed'),
        ('purchase', 'Purchase Made'),
        ('review_posted', 'Review Posted'),
        ('other', 'Other Activity'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    description = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'accounts_user_activity'
        indexes = [
            models.Index(fields=['user', 'activity_type']),
            models.Index(fields=['timestamp']),
        ]
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()}"


# Signal handlers for automatic profile creation
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create UserProfile when User is created"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_vendor_profile(sender, instance, created, **kwargs):
    """Create VendorProfile when vendor User is created"""
    if created and instance.user_type == 'vendor':
        VendorProfile.objects.create(
            user=instance,
            business_name=f"{instance.username}'s Business",
            shop_name=f"{instance.username}'s Shop",
            shop_description="Welcome to our shop!",
            business_type='sole_proprietor',
            shop_category='general',
            physical_address='Nairobi, Kenya',
            business_phone=instance.phone_number
        )


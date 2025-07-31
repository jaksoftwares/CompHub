# Dovepeak CompHub - Nairobi's Smart IT Marketplace

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Django](https://img.shields.io/badge/django-4.2+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-in_development-orange.svg)

A comprehensive multi-vendor ecommerce platform connecting verified electronics and IT product vendors across Nairobi with customers seeking trusted, convenient access to quality products.

## 🚀 Project Overview

Dovepeak CompHub digitizes Nairobi's electronics retail sector by creating a trusted marketplace where customers can easily find and purchase computers, laptops, smartphones, gadgets, and IT accessories from verified local vendors. The platform eliminates the need for customers to physically visit multiple shops on busy streets like Moi Avenue, Luthuli Avenue, and Kimathi Street.

### Key Features

- **Multi-vendor marketplace** with verified sellers
- **Token-based listing system** for vendors
- **Advanced product filtering** and search capabilities
- **Integrated payment system** (M-Pesa, Card payments)
- **Shop location mapping** for in-person visits
- **Comprehensive vendor verification** (KYC process)
- **Review and rating system** for trust building
- **Mobile-responsive design** for all devices

## 🎯 Target Users

### Buyers (Customers)
- Tech enthusiasts and professionals
- Students and educational institutions
- Small and medium businesses
- Individual consumers seeking IT products

### Vendors (Retailers)
- Electronics shop owners in Nairobi
- IT product distributors
- Mobile device retailers
- Computer repair services
- Accessory suppliers

### Platform Administrators
- Dovepeak team members
- Customer support representatives
- Content moderators

## 🛠 Technology Stack

### Backend
- **Python 3.9+**
- **Django 4.2+** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Primary database
- **Redis** - Caching and session storage
- **Celery** - Asynchronous task processing

### Frontend
- **HTML5/CSS3**
- **JavaScript (ES6+)**
- **Bootstrap 5** - UI framework
- **HTMX** - Dynamic interactions
- **Chart.js** - Analytics dashboards

### Payment Integration
- **M-Pesa API** - Mobile money payments
- **Stripe** - Card payments
- **PayPal** - International payments

### Infrastructure
- **Docker** - Containerization
- **AWS/DigitalOcean** - Cloud hosting
- **Cloudinary** - Image storage and optimization
- **Sentry** - Error monitoring

## 📁 Project Structure

```
dovepeak_comphub/
├── accounts/           # User authentication and profiles
├── admin_panel/        # Platform administration
├── analytics/          # Business intelligence and reporting
├── core/              # Shared utilities and configurations
├── notifications/     # Messaging and alerts system
├── orders/            # Order processing and management
├── payments/          # Token system and payment processing
├── products/          # Product catalog and inventory
├── reviews/           # Rating and review system
├── vendors/           # Vendor management and verification
├── static/            # CSS, JavaScript, images
├── templates/         # HTML templates
├── media/             # User-uploaded files
├── requirements/      # Python dependencies
├── config/            # Django settings
└── manage.py
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- PostgreSQL 12+
- Redis 6+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/dovepeak-comphub.git
   cd dovepeak-comphub
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements/local.txt
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Load initial data**
   ```bash
   python manage.py loaddata fixtures/categories.json
   python manage.py loaddata fixtures/locations.json
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Start background services**
   ```bash
   # Terminal 2: Redis
   redis-server
   
   # Terminal 3: Celery
   celery -A config worker -l info
   ```

Visit `http://localhost:8000` to access the application.

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dovepeak_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# M-Pesa Configuration
MPESA_CONSUMER_KEY=your-mpesa-consumer-key
MPESA_CONSUMER_SECRET=your-mpesa-consumer-secret
MPESA_SHORTCODE=your-business-shortcode

# File Storage
CLOUDINARY_NAME=your-cloudinary-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Security
SENTRY_DSN=your-sentry-dsn
```

## 📊 Database Schema

### Core Models

- **User** - Extended authentication with buyer/vendor/admin roles
- **UserProfile** - Personal information and preferences
- **VendorProfile** - Business details and shop information
- **Product** - Product catalog with specifications
- **Order** - Purchase transactions and fulfillment
- **Payment** - Token purchases and financial records
- **Review** - Customer feedback and ratings

### Key Relationships

- Users can be buyers, vendors, or administrators
- Vendors have detailed business profiles and token balances
- Products belong to vendor shops and categories
- Orders connect buyers with vendor products
- Reviews link buyers to purchased products

## 🔐 Security Features

- **User verification system** with KYC document upload
- **Multi-factor authentication** support
- **Rate limiting** on API endpoints
- **CSRF protection** on all forms
- **SQL injection prevention** through ORM
- **File upload validation** and scanning
- **Activity logging** for audit trails

## 💳 Token System

Vendors use tokens to list and promote products:

- **Listing tokens** - Required to create product listings
- **Promotion tokens** - Boost product visibility
- **Token packages** - Bulk purchase discounts
- **Auto-renewal** - Subscription-based token refills

### Token Pricing (Sample)
- Basic Package: 100 tokens - KES 1,000
- Standard Package: 500 tokens - KES 4,500
- Premium Package: 1,000 tokens - KES 8,000

## 📱 API Documentation

RESTful API endpoints for mobile app integration:

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/verify-phone/` - Phone verification

### Products
- `GET /api/products/` - List products
- `GET /api/products/{id}/` - Product details
- `GET /api/categories/` - Product categories

### Vendors
- `GET /api/vendors/` - List verified vendors
- `GET /api/vendors/{id}/` - Vendor profile

### Orders
- `POST /api/orders/` - Create order
- `GET /api/orders/` - User order history

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 📈 Performance Monitoring

- **Database query optimization** with Django Debug Toolbar
- **Caching strategy** using Redis for frequent queries
- **Image optimization** through Cloudinary
- **CDN integration** for static assets
- **Background task processing** with Celery

## 🚢 Deployment

### Production Setup

1. **Environment preparation**
   ```bash
   pip install -r requirements/production.txt
   python manage.py collectstatic
   python manage.py migrate
   ```

2. **Docker deployment**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Load balancer configuration**
   - Nginx reverse proxy
   - SSL certificate setup
   - Static file serving

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write comprehensive tests
- Update documentation
- Use meaningful commit messages
- Code review required for all PRs

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- [Developer Guide](docs/developer-guide.md)
- [API Reference](docs/api-reference.md)
- [Deployment Guide](docs/deployment.md)

### Community
- **Email**: support@dovepeak.co.ke
- **Phone**: +254-XXX-XXXXXX
- **Issues**: [GitHub Issues](https://github.com/your-username/dovepeak-comphub/issues)

## 🗺 Roadmap

### Phase 1 (Q3 2025)
- ✅ Core marketplace functionality
- ✅ Vendor registration and verification
- ✅ Product catalog and search
- ✅ Basic payment integration

### Phase 2 (Q4 2025)
- 🔄 Mobile applications (iOS/Android)
- 🔄 Advanced analytics dashboard
- 🔄 AI-powered recommendations
- 🔄 Delivery integration

### Phase 3 (Q1 2026)
- ⏳ Multi-city expansion
- ⏳ B2B procurement portal
- ⏳ Vendor subscription tiers
- ⏳ Affiliate marketing program

### Phase 4 (Q2 2026)
- ⏳ International shipping
- ⏳ Cryptocurrency payments
- ⏳ AR product visualization
- ⏳ Vendor analytics AI

## 📊 Project Metrics

- **Target Vendors**: 500+ verified shops
- **Expected Products**: 10,000+ listings
- **Projected Users**: 50,000+ registered buyers
- **Coverage Area**: Nairobi County (expanding to other counties)

## 🏆 Achievements

- 🎯 Solving real market problems in Nairobi's electronics sector
- 💼 Empowering small and medium IT retailers
- 🛡️ Building trust through verification systems
- 📱 Modern user experience for traditional market

---

**Built with ❤️ in Nairobi, Kenya**

*Transforming how Nairobi shops for technology, one click at a time.*
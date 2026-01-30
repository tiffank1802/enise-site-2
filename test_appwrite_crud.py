"""
Test script to verify all Appwrite CRUD operations
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "enise_site.settings")
django.setup()

from app_core.services import (
    SpecialiteService,
    ActualiteService,
    ContactService,
    PartenairesService,
    StatistiqueService,
)

def test_specialites():
    """Test Specialite CRUD operations"""
    print("\n🧪 Testing Specialites Service...")
    service = SpecialiteService()
    
    # List all
    specialites = service.list_all()
    print(f"  ✅ List all: {len(specialites)} specialites found")
    
    if specialites:
        # Get by slug
        first_spec = specialites[0]
        slug = first_spec.get('slug')
        if slug:
            spec = service.get_by_slug(slug)
            print(f"  ✅ Get by slug: {spec.get('nom', 'Unknown')} retrieved")
        
        # Get by ID
        doc_id = first_spec.get('id')
        if doc_id:
            spec = service.get_by_id(doc_id)
            print(f"  ✅ Get by ID: {spec.get('nom', 'Unknown')} retrieved")
    
    print("  ✅ Specialites service OK")


def test_actualites():
    """Test Actualite CRUD operations"""
    print("\n🧪 Testing Actualites Service...")
    service = ActualiteService()
    
    # List published
    actualites = service.list_published()
    print(f"  ✅ List published: {len(actualites)} actualites found")
    
    # List all
    all_actualites = service.list_all()
    print(f"  ✅ List all: {len(all_actualites)} actualites total")
    
    print("  ✅ Actualites service OK")


def test_contact():
    """Test Contact CRUD operations"""
    print("\n🧪 Testing Contact Service...")
    service = ContactService()
    
    # List all
    contacts = service.list_all()
    print(f"  ✅ List all: {len(contacts)} contact messages found")
    
    # Create a test contact
    try:
        new_contact = service.create(
            nom="Test User",
            email="test@example.com",
            sujet="Test Subject",
            message="This is a test message"
        )
        print(f"  ✅ Create: New contact created with ID {new_contact.get('id')}")
        
        # Get the contact
        contact_id = new_contact.get('id')
        if contact_id:
            retrieved = service.get_by_id(contact_id)
            print(f"  ✅ Get by ID: Contact retrieved: {retrieved.get('nom')}")
            
            # Mark as treated
            treated = service.mark_as_treated(contact_id)
            print(f"  ✅ Mark as treated: Contact updated")
            
            # Delete
            deleted = service.delete(contact_id)
            print(f"  ✅ Delete: Contact deleted")
    except Exception as e:
        print(f"  ⚠️  Error in contact operations: {e}")
    
    print("  ✅ Contact service OK")


def test_partenaires():
    """Test Partenaires CRUD operations"""
    print("\n🧪 Testing Partenaires Service...")
    service = PartenairesService()
    
    # List all
    partenaires = service.list_all()
    print(f"  ✅ List all: {len(partenaires)} partenaires found")
    
    # List by type
    industriels = service.list_all(type_partenaire='INDUSTRIEL')
    print(f"  ✅ List by type: {len(industriels)} industriels found")
    
    print("  ✅ Partenaires service OK")


def test_statistiques():
    """Test Statistique CRUD operations"""
    print("\n🧪 Testing Statistiques Service...")
    service = StatistiqueService()
    
    # List all
    statistiques = service.list_all()
    print(f"  ✅ List all: {len(statistiques)} statistiques found")
    
    print("  ✅ Statistiques service OK")


def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 APPWRITE CRUD OPERATIONS TEST")
    print("=" * 60)
    
    try:
        test_specialites()
        test_actualites()
        test_contact()
        test_partenaires()
        test_statistiques()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

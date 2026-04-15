"""
Database Seed Script
Initializes MongoDB with mock data for development and testing.

Usage:
    python3 database/seed.py              # Interactive mode
    python3 database/seed.py --reset      # Force reset and seed
    python3 database/seed.py --dry-run    # Preview without writing
"""

import asyncio
import os
import sys
from datetime import datetime, timezone
from uuid import uuid4
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import User, Survey, Question, Response, Answer

load_dotenv()

MONGODB_URI = os.getenv('DB_CONNECTION_STRING', 'mongodb://admin:password@localhost:27017')


async def seed_database(reset: bool = True, dry_run: bool = False):
    """Seed database with mock data
    
    Args:
        reset: If True, clear existing data before seeding
        dry_run: If True, don't write to database (preview only)
    """
    
    # Connect to database
    client = AsyncIOMotorClient(MONGODB_URI)
    database = client["local"]
    
    await init_beanie(
        database=database,
        document_models=[User, Survey, Question, Response, Answer]
    )
    
    print("🗄️  Connected to MongoDB")
    
    # Clean existing data
    if reset:
        print("🧹 Cleaning existing data...")
        if not dry_run:
            await User.delete_all()
            await Survey.delete_all()
            await Question.delete_all()
            await Response.delete_all()
            await Answer.delete_all()
            print("   ✅ Database cleared")
    
    # ==================== CREATE USERS ====================
    print("\n👥 Creating users...")
    
    users = [
        User(
            email="alice@example.com",
            name="Alice Johnson",
            google_id="google_alice_123"
        ),
        User(
            email="bob@example.com",
            name="Bob Smith",
            google_id="google_bob_456"
        ),
        User(
            email="carol@example.com",
            name="Carol White",
            google_id="google_carol_789"
        ),
    ]
    
    if not dry_run:
        await User.insert_many(users)
    print(f"   ✅ Created {len(users)} users")
    user_ids = [u.id for u in users]
    
    # ==================== CREATE SURVEYS ====================
    print("\n📋 Creating surveys...")
    
    survey1_id = str(uuid4())
    survey2_id = str(uuid4())
    survey3_id = str(uuid4())
    
    surveys = [
        Survey(
            id=survey1_id,
            title="Customer Satisfaction Survey",
            description="Help us improve our service by sharing your feedback",
            created_by=str(user_ids[0]),
            is_published=True,
        ),
        Survey(
            id=survey2_id,
            title="Product Feature Feedback",
            description="What features would you like to see next?",
            created_by=str(user_ids[0]),
            is_published=True,
        ),
        Survey(
            id=survey3_id,
            title="Employee Satisfaction Survey",
            description="Anonymous feedback for our team",
            created_by=str(user_ids[1]),
            is_published=True,
        ),
    ]
    
    if not dry_run:
        await Survey.insert_many(surveys)
    print(f"   ✅ Created {len(surveys)} surveys")
    
    # ==================== CREATE QUESTIONS ====================
    print("\n❓ Creating questions...")
    
    # Survey 1 questions
    survey1_q1_id = str(uuid4())
    survey1_q2_id = str(uuid4())
    survey1_q3_id = str(uuid4())
    
    # Survey 2 questions
    survey2_q1_id = str(uuid4())
    survey2_q2_id = str(uuid4())
    
    # Survey 3 questions
    survey3_q1_id = str(uuid4())
    survey3_q2_id = str(uuid4())
    
    questions = [
        # Survey 1 questions
        Question(
            id=survey1_q1_id,
            survey_id=survey1_id,
            question="How satisfied are you with our service?",
            type="rating",
            choices=["Very Unsatisfied", "Unsatisfied", "Neutral", "Satisfied", "Very Satisfied"],
            required=True,
            order=1,
        ),
        Question(
            id=survey1_q2_id,
            survey_id=survey1_id,
            question="What could we improve?",
            type="text",
            choices=[],
            required=False,
            order=2,
        ),
        Question(
            id=survey1_q3_id,
            survey_id=survey1_id,
            question="Which aspects did you like the most? (select all that apply)",
            type="checkbox",
            choices=["Product Quality", "Customer Support", "Price", "Delivery Speed", "Packaging"],
            required=False,
            order=3,
        ),
        # Survey 2 questions
        Question(
            id=survey2_q1_id,
            survey_id=survey2_id,
            question="What is your primary use case?",
            type="multiple_choice",
            choices=["Personal", "Business", "Educational", "Other"],
            required=True,
            order=1,
        ),
        Question(
            id=survey2_q2_id,
            survey_id=survey2_id,
            question="Describe the feature you'd like to see:",
            type="text",
            choices=[],
            required=True,
            order=2,
        ),
        # Survey 3 questions
        Question(
            id=survey3_q1_id,
            survey_id=survey3_id,
            question="I feel valued in my role",
            type="rating",
            choices=["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"],
            required=True,
            order=1,
        ),
        Question(
            id=survey3_q2_id,
            survey_id=survey3_id,
            question="Which benefits are most important to you?",
            type="checkbox",
            choices=["Health Insurance", "Remote Work", "Flexible Hours", "Professional Development", "Stock Options"],
            required=False,
            order=2,
        ),
    ]
    
    if not dry_run:
        await Question.insert_many(questions)
    print(f"   ✅ Created {len(questions)} questions")
    
    # ==================== CREATE RESPONSES & ANSWERS ====================
    print("\n📝 Creating responses and answers...")
    
    responses = []
    answers = []
    
    # Response 1 - Alice to Survey 1
    response1_id = str(uuid4())
    responses.append(Response(
        id=response1_id,
        survey_id=survey1_id,
        user_id=str(user_ids[0]),
    ))
    answers.extend([
        Answer(
            response_id=response1_id,
            question_id=survey1_q1_id,
            answer=["Very Satisfied"],
        ),
        Answer(
            response_id=response1_id,
            question_id=survey1_q2_id,
            answer=["The documentation could be more detailed."],
        ),
        Answer(
            response_id=response1_id,
            question_id=survey1_q3_id,
            answer=["Customer Support", "Delivery Speed"],
        ),
    ])
    
    # Response 2 - Bob to Survey 1
    response2_id = str(uuid4())
    responses.append(Response(
        id=response2_id,
        survey_id=survey1_id,
        user_id=str(user_ids[1]),
    ))
    answers.extend([
        Answer(
            response_id=response2_id,
            question_id=survey1_q1_id,
            answer=["Satisfied"],
        ),
        Answer(
            response_id=response2_id,
            question_id=survey1_q2_id,
            answer=["More features would be helpful."],
        ),
        Answer(
            response_id=response2_id,
            question_id=survey1_q3_id,
            answer=["Product Quality", "Price"],
        ),
    ])
    
    # Response 3 - Carol to Survey 2
    response3_id = str(uuid4())
    responses.append(Response(
        id=response3_id,
        survey_id=survey2_id,
        user_id=str(user_ids[2]),
    ))
    answers.extend([
        Answer(
            response_id=response3_id,
            question_id=survey2_q1_id,
            answer=["Business"],
        ),
        Answer(
            response_id=response3_id,
            question_id=survey2_q2_id,
            answer=["Integration with third-party APIs would be great."],
        ),
    ])
    
    # Response 4 - Alice to Survey 3
    response4_id = str(uuid4())
    responses.append(Response(
        id=response4_id,
        survey_id=survey3_id,
        user_id=str(user_ids[0]),
    ))
    answers.extend([
        Answer(
            response_id=response4_id,
            question_id=survey3_q1_id,
            answer=["Agree"],
        ),
        Answer(
            response_id=response4_id,
            question_id=survey3_q2_id,
            answer=["Professional Development", "Flexible Hours"],
        ),
    ])
    
    # Response 5 - Anonymous response to Survey 1
    response5_id = str(uuid4())
    responses.append(Response(
        id=response5_id,
        survey_id=survey1_id,
        user_id=None,  # Anonymous
    ))
    answers.extend([
        Answer(
            response_id=response5_id,
            question_id=survey1_q1_id,
            answer=["Neutral"],
        ),
        Answer(
            response_id=response5_id,
            question_id=survey1_q2_id,
            answer=["Everything is fine."],
        ),
        Answer(
            response_id=response5_id,
            question_id=survey1_q3_id,
            answer=["Product Quality"],
        ),
    ])
    
    if not dry_run:
        await Response.insert_many(responses)
        await Answer.insert_many(answers)
    
    print(f"   ✅ Created {len(responses)} responses")
    print(f"   ✅ Created {len(answers)} answers")
    
    # ==================== SUMMARY ====================
    print("\n" + "="*60)
    if dry_run:
        print("🔍 DRY RUN - NO DATA WRITTEN TO DATABASE")
    else:
        print("✅ MOCK DATA CREATED SUCCESSFULLY")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"   • Users:        {len(users)}")
    print(f"   • Surveys:      {len(surveys)}")
    print(f"   • Questions:    {len(questions)}")
    print(f"   • Responses:    {len(responses)}")
    print(f"   • Answers:      {len(answers)}")
    
    print(f"\n📋 Survey IDs for testing:")
    print(f"   • Customer Satisfaction:  {survey1_id}")
    print(f"   • Product Features:       {survey2_id}")
    print(f"   • Employee Satisfaction: {survey3_id}")
    
    print(f"\n👥 User credentials:")
    for user in users:
        print(f"   • {user.name} ({user.email})")
    
    print("\n💡 You can now use the frontend to:")
    print("   • View surveys")
    print("   • Fill out survey forms")
    print("   • See responses and analytics")
    
    # Close connection
    client.close()
    print("\n✅ Done!")


async def interactive_mode():
    """Interactive mode for seed operations"""
    print("\n" + "="*60)
    print("DATABASE SEED SCRIPT")
    print("="*60)
    print("\nOptions:")
    print("  1. Seed database (reset existing data)")
    print("  2. Seed database (keep existing data)")
    print("  3. Dry run (preview only)")
    print("  4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        await seed_database(reset=True, dry_run=False)
    elif choice == "2":
        await seed_database(reset=False, dry_run=False)
    elif choice == "3":
        await seed_database(reset=False, dry_run=True)
    elif choice == "4":
        print("Exiting...")
    else:
        print("Invalid choice")


if __name__ == "__main__":
    if "--reset" in sys.argv:
        asyncio.run(seed_database(reset=True, dry_run=False))
    elif "--dry-run" in sys.argv:
        asyncio.run(seed_database(reset=False, dry_run=True))
    elif "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
    else:
        asyncio.run(interactive_mode())

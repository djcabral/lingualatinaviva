import sys
import os
from sqlmodel import Session, select, func

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connection import engine
from database import UserProfile, ReviewLog, Word

def diagnose():
    print("=== Diagnóstico del Sistema de Usuario ===\n")
    
    with Session(engine) as session:
        # Check UserProfile
        users = session.exec(select(UserProfile)).all()
        print(f"📊 Usuarios en la base de datos: {len(users)}")
        for user in users:
            print(f"   - ID: {user.id}, Username: {user.username}, Level: {user.level}, XP: {user.xp}")
        
        if not users:
            print("   ⚠️  NO HAY USUARIOS. Esto explicaría por qué no se registran intentos.")
            print("   La app debería crear automáticamente un usuario 'Discipulus'.")
        
        print()
        
        # Check ReviewLogs
        review_count = session.exec(select(func.count()).select_from(ReviewLog)).one()
        print(f"📝 ReviewLogs en la base de datos: {review_count}")
        
        if review_count > 0:
            recent = session.exec(
                select(ReviewLog).order_by(ReviewLog.review_date.desc()).limit(5)
            ).all()
            print("   Últimos 5 registros:")
            for r in recent:
                print(f"   - Word ID: {r.word_id}, Date: {r.review_date}, Quality: {r.quality}")
        else:
            print("   ⚠️  NO HAY REVIEW LOGS registrados.")
        
        print()
        
        # Check Words
        word_count = session.exec(select(func.count()).select_from(Word)).one()
        print(f"📚 Palabras en la base de datos: {word_count}")

if __name__ == "__main__":
    diagnose()

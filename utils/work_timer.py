
import time
import sys
import json
import os
from datetime import datetime, timedelta

STATE_FILE = ".timer_state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                data = json.load(f)
            # Check if it's from today
            saved_date = data.get('date')
            today = datetime.now().strftime('%Y-%m-%d')
            if saved_date == today:
                return data
        except:
            pass
    return None

def save_state(elapsed, target):
    data = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'elapsed': elapsed,
        'target': target,
        'last_updated': datetime.now().strftime('%H:%M:%S')
    }
    with open(STATE_FILE, 'w') as f:
        json.dump(data, f)

def work_timer(target_hours=8.0):
    total_seconds = target_hours * 3600
    
    # Try to resume
    state = load_state()
    elapsed_seconds = 0.0
    
    if state:
        elapsed_seconds = state.get('elapsed', 0.0)
        print(f"\n🔄 RESUMIENDO SESIÓN DE HOY")
        print(f"📊 Progreso guardado: {timedelta(seconds=int(elapsed_seconds))}")
    else:
        print(f"\n☀️ NUEVA SESIÓN")
    
    start_time = datetime.now()
    # Estimate finish time based on remaining work
    remaining_seconds = max(0, total_seconds - elapsed_seconds)
    finish_time = start_time + timedelta(seconds=remaining_seconds)
    
    print(f"🎯 META: {target_hours} horas")
    print(f"🛑 HORA ESTIMADA DE SALIDA: {finish_time.strftime('%H:%M')}")
    print("-" * 40 + "\n")
    
    try:
        while True:
            # We track "session elapsed" + "previously elapsed"
            current_session_elapsed = (datetime.now() - start_time).total_seconds()
            total_elapsed = elapsed_seconds + current_session_elapsed
            
            remaining = total_seconds - total_elapsed
            
            # Save state every 5 seconds or if done
            if int(total_elapsed) % 5 == 0:
                save_state(total_elapsed, target_hours)

            if remaining <= 0:
                save_state(total_elapsed, target_hours)
                print("\n\n" + "="*40)
                print("🚨 ¡JORNADA COMPLETADA! 🚨")
                print("Has cumplido tus horas de hoy.")
                print("="*40 + "\n")
                print('\a') # Beep
                break
                
            # Render Bar
            percent = min(100, (total_elapsed / total_seconds) * 100)
            bar_length = 30
            filled_length = int(bar_length * percent // 100)
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            
            rem_str = str(timedelta(seconds=int(remaining)))
            
            sys.stdout.write(f"\r[{bar}] {percent:.1f}% | Restan: {rem_str}")
            sys.stdout.flush()
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        # Save on exit
        current_session_elapsed = (datetime.now() - start_time).total_seconds()
        save_state(elapsed_seconds + current_session_elapsed, target_hours)
        print("\n\n💾 Progreso guardado. ¡Hasta luego!")

if __name__ == "__main__":
    try:
        h = float(sys.argv[1]) if len(sys.argv) > 1 else 8.0
    except ValueError:
        h = 8.0
    work_timer(h)

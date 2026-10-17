"""
ContextPilot AI — Automated High-Resolution Screenshot Capture Utility
Captures 23 authentic views across all routes, tabs, modals, and interactive states.
"""

import os
import sys
import time
import json
import subprocess
import urllib.request
import urllib.error
from playwright.sync_api import sync_playwright

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(WORKSPACE, "backend")
FRONTEND_DIR = os.path.join(WORKSPACE, "frontend")
IMAGES_DIR = os.path.join(WORKSPACE, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

PYTHON_EXE = os.path.join(BACKEND_DIR, ".venv", "Scripts", "python.exe")
if not os.path.exists(PYTHON_EXE):
    PYTHON_EXE = sys.executable

def wait_for_url(url, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=2) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.8)
    return False

def post_json(url, data, token=None):
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            **({"Authorization": f"Bearer {token}"} if token else {})
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode("utf-8"))
        except Exception:
            return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def nav_and_wait(page, url, delay=1.2):
    page.goto(url, wait_until="domcontentloaded", timeout=15000)
    try:
        page.wait_for_selector("text=Authenticating session...", state="hidden", timeout=8000)
    except Exception:
        pass
    time.sleep(delay)

def main():
    print("[1/5] Launching backend server on 127.0.0.1:8000...")
    backend_proc = subprocess.Popen(
        [PYTHON_EXE, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=BACKEND_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    print("[2/5] Launching frontend Vite server on 127.0.0.1:5173...")
    frontend_proc = subprocess.Popen(
        "npm run dev -- --host 127.0.0.1 --port 5173",
        cwd=FRONTEND_DIR,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    try:
        print("[3/5] Waiting for services to respond...")
        if not wait_for_url("http://127.0.0.1:8000/health", timeout=25):
            raise RuntimeError("Backend failed to start on http://127.0.0.1:8000")
        if not wait_for_url("http://127.0.0.1:5173", timeout=25):
            raise RuntimeError("Frontend failed to start on http://127.0.0.1:5173")
        print(" -> Services are live.")

        print("[4/5] Creating & seeding demo account...")
        post_json("http://127.0.0.1:8000/api/v1/auth/register", {
            "email": "pilot@contextpilot.ai",
            "password": "DemoPassword123!",
            "full_name": "Demo Pilot"
        })
        
        login_res = post_json("http://127.0.0.1:8000/api/v1/auth/login", {
            "email": "pilot@contextpilot.ai",
            "password": "DemoPassword123!"
        })
        token = login_res.get("access_token")
        if not token:
            print("Failed to acquire token:", login_res)
            return

        seed_res = post_json("http://127.0.0.1:8000/api/v1/demo/seed", {}, token=token)
        print(" -> Demo data seeded:", seed_res.get("message", "OK"))

        user_req = urllib.request.Request(
            "http://127.0.0.1:8000/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        with urllib.request.urlopen(user_req, timeout=5) as resp:
            user_data = json.loads(resp.read().decode("utf-8"))

        print("[5/5] Starting Playwright & capturing 23 section screenshots...")
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="msedge", headless=True)
            context = browser.new_context(
                viewport={"width": 1440, "height": 900},
                device_scale_factor=1.5
            )
            page = context.new_page()
            page.set_default_timeout(15000)

            # Helper for injecting auth
            def inject_auth():
                page.evaluate(f"""() => {{
                    localStorage.setItem('token', '{token}');
                    localStorage.setItem('user', JSON.stringify({json.dumps(user_data)}));
                }}""")

            # ---------------- PUBLIC PAGES ----------------
            # 01. Landing Hero
            print(" -> 01_landing_page.png...")
            page.goto("http://127.0.0.1:5173", wait_until="domcontentloaded")
            time.sleep(1.2)
            page.screenshot(path=os.path.join(IMAGES_DIR, "01_landing_page.png"))

            # 02. Landing Features & Architecture
            print(" -> 02_landing_features.png...")
            page.evaluate("window.scrollTo(0, 850)")
            time.sleep(1)
            page.screenshot(path=os.path.join(IMAGES_DIR, "02_landing_features.png"))

            # 03. Login Page
            print(" -> 03_login_page.png...")
            page.goto("http://127.0.0.1:5173/login", wait_until="domcontentloaded")
            time.sleep(0.8)
            demo_btn = page.locator("button:has-text('Auto-Fill Demo Credentials'), button:has-text('Fill Demo Account')")
            if demo_btn.count() > 0:
                demo_btn.first.click()
            time.sleep(0.5)
            page.screenshot(path=os.path.join(IMAGES_DIR, "03_login_page.png"))

            # 04. Register Page
            print(" -> 04_register_page.png...")
            page.goto("http://127.0.0.1:5173/register", wait_until="domcontentloaded")
            time.sleep(0.8)
            page.screenshot(path=os.path.join(IMAGES_DIR, "04_register_page.png"))

            # 05. Privacy Policy
            print(" -> 05_privacy_policy.png...")
            page.goto("http://127.0.0.1:5173/privacy", wait_until="domcontentloaded")
            time.sleep(0.8)
            page.screenshot(path=os.path.join(IMAGES_DIR, "05_privacy_policy.png"))

            # 06. Terms of Service
            print(" -> 06_terms_of_service.png...")
            page.goto("http://127.0.0.1:5173/terms", wait_until="domcontentloaded")
            time.sleep(0.8)
            page.screenshot(path=os.path.join(IMAGES_DIR, "06_terms_of_service.png"))

            # ---------------- AUTHENTICATED APP WORKSPACE ----------------
            inject_auth()

            # 07. Dashboard Overview
            print(" -> 07_dashboard_overview.png...")
            nav_and_wait(page, "http://127.0.0.1:5173/app", delay=1.8)
            page.screenshot(path=os.path.join(IMAGES_DIR, "07_dashboard_overview.png"))

            # 08. Assistant Workspace & Active Plan
            print(" -> 08_assistant_chat.png...")
            nav_and_wait(page, "http://127.0.0.1:5173/app/assistant", delay=1.8)
            page.screenshot(path=os.path.join(IMAGES_DIR, "08_assistant_chat.png"))

            # 09. Assistant Multi-Step Execution Conversation
            print(" -> 09_assistant_active_execution.png...")
            try:
                chat_input = page.locator("input[placeholder*='objective'], textarea, input[type='text']").last
                if chat_input.count() > 0:
                    chat_input.fill("Calculate quarterly cloud runway and summarize key findings")
                    time.sleep(0.3)
                    send_btn = page.locator("button[type='submit']")
                    if send_btn.count() > 0:
                        send_btn.first.click()
                        time.sleep(2.5)
            except Exception as e:
                print("Note on assistant interaction:", e)
            page.screenshot(path=os.path.join(IMAGES_DIR, "09_assistant_active_execution.png"))

            # 10. Task Workflows Monitor
            print(" -> 10_task_workflows.png...")
            nav_and_wait(page, "http://127.0.0.1:5173/app/tasks", delay=1.8)
            page.screenshot(path=os.path.join(IMAGES_DIR, "10_task_workflows.png"))

            # 11. Task Detail with Human Approval Gate
            print(" -> 11_task_detail_approval.png...")
            task_cards = page.locator("a[href*='/app/tasks/']")
            if task_cards.count() > 1:
                task_cards.nth(1).click()
                time.sleep(1.8)
            elif task_cards.count() > 0:
                task_cards.first.click()
                time.sleep(1.8)
            page.screenshot(path=os.path.join(IMAGES_DIR, "11_task_detail_approval.png"))

            # 12. Knowledge Base & Grounded RAG Overview
            print(" -> 12_knowledge_rag.png...")
            nav_and_wait(page, "http://127.0.0.1:5173/app/knowledge", delay=1.8)
            page.screenshot(path=os.path.join(IMAGES_DIR, "12_knowledge_rag.png"))

            # 13. Grounded RAG Query Sandbox with Verifiable Citations
            print(" -> 13_knowledge_rag_search.png...")
            try:
                rag_input = page.locator("input[placeholder*='What does the guide say']")
                if rag_input.count() > 0:
                    rag_input.fill("What are the rules for human approval before tool execution?")
                    time.sleep(0.3)
                    ask_btn = page.locator("button:has-text('Ask Knowledge Base')")
                    if ask_btn.count() > 0:
                        ask_btn.click()
                        time.sleep(2)
            except Exception as e:
                print("Note on RAG query:", e)
            page.screenshot(path=os.path.join(IMAGES_DIR, "13_knowledge_rag_search.png"))

            # 14. Context Memory Hub
            print(" -> 14_memory_hub.png...")
            nav_and_wait(page, "http://127.0.0.1:5173/app/memory", delay=1.8)
            page.screenshot(path=os.path.join(IMAGES_DIR, "14_memory_hub.png"))

            # 15. Sandboxed Tool Safety Registry
            print(" -> 15_tool_registry.png...")
            nav_and_wait(page, "http://127.0.0.1:5173/app/tools", delay=1.8)
            page.screenshot(path=os.path.join(IMAGES_DIR, "15_tool_registry.png"))

            # 16. Interactive Tool Testbench Modal
            print(" -> 16_tool_testbench_modal.png...")
            try:
                test_btn = page.locator("button:has-text('Test Tool')").first
                if test_btn.count() > 0:
                    test_btn.click()
                    time.sleep(0.8)
                    run_exec_btn = page.locator("button:has-text('Run Execution')")
                    if run_exec_btn.count() > 0:
                        run_exec_btn.click()
                        time.sleep(1.5)
            except Exception as e:
                print("Note on Tool Testbench:", e)
            page.screenshot(path=os.path.join(IMAGES_DIR, "16_tool_testbench_modal.png"))
            # Close modal if open
            try:
                cancel_btn = page.locator("button:has-text('Cancel'), button:has-text('Close')")
                if cancel_btn.count() > 0:
                    cancel_btn.first.click()
                    time.sleep(0.5)
            except Exception:
                pass

            # 17. Activity & Audit Trail
            print(" -> 17_activity_audit.png...")
            nav_and_wait(page, "http://127.0.0.1:5173/app/activity", delay=1.8)
            page.screenshot(path=os.path.join(IMAGES_DIR, "17_activity_audit.png"))

            # 18. Notifications Tab
            print(" -> 18_activity_notifications.png...")
            try:
                notif_tab = page.locator("button:has-text('Notifications')")
                if notif_tab.count() > 0:
                    notif_tab.click()
                    time.sleep(1)
            except Exception as e:
                print("Note on Notification tab:", e)
            page.screenshot(path=os.path.join(IMAGES_DIR, "18_activity_notifications.png"))

            # 19. Real-Time Analytics & Telemetry (Recharts)
            print(" -> 19_analytics_telemetry.png...")
            nav_and_wait(page, "http://127.0.0.1:5173/app/analytics", delay=2.5)
            page.screenshot(path=os.path.join(IMAGES_DIR, "19_analytics_telemetry.png"))

            # 20. Settings: User Profile
            print(" -> 20_settings_profile.png...")
            nav_and_wait(page, "http://127.0.0.1:5173/app/settings", delay=1.8)
            page.screenshot(path=os.path.join(IMAGES_DIR, "20_settings_profile.png"))

            # 21. Settings: Assistant Preferences
            print(" -> 21_settings_assistant.png...")
            try:
                asst_pref_btn = page.locator("button:has-text('Assistant Preferences')")
                if asst_pref_btn.count() > 0:
                    asst_pref_btn.click()
                    time.sleep(1)
            except Exception as e:
                print("Note on Assistant Preferences tab:", e)
            page.screenshot(path=os.path.join(IMAGES_DIR, "21_settings_assistant.png"))

            # 22. Settings: Model Providers & AWS Bedrock
            print(" -> 22_settings_provider.png...")
            try:
                integ_btn = page.locator("button:has-text('Integrations & AWS'), button:has-text('Integrations')")
                if integ_btn.count() > 0:
                    integ_btn.click()
                    time.sleep(1)
            except Exception as e:
                print("Note on Integrations tab:", e)
            page.screenshot(path=os.path.join(IMAGES_DIR, "22_settings_provider.png"))

            # 23. Help & Agent Architecture Documentation
            print(" -> 23_help_guide.png...")
            nav_and_wait(page, "http://127.0.0.1:5173/app/help", delay=1.8)
            page.screenshot(path=os.path.join(IMAGES_DIR, "23_help_guide.png"))

            browser.close()

        print("[6/6] All 23 screenshots captured successfully!")

    finally:
        print("Cleaning up processes...")
        try:
            backend_proc.terminate()
            backend_proc.kill()
        except Exception:
            pass
        try:
            frontend_proc.terminate()
            frontend_proc.kill()
        except Exception:
            pass

if __name__ == "__main__":
    main()

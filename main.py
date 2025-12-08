"""
🚀 REAL Facebook End-to-End Automation
Complete working - Login to Message sending
"""

import streamlit as st
import time
import json
import pickle
import random
from datetime import datetime
from pathlib import Path
import sys
import subprocess
import os

# ============================================
# AUTO-INSTALLATION SYSTEM
# ============================================

def install_required_packages():
    """Auto-install required packages"""
    try:
        # Try to import selenium
        from selenium import webdriver
        print("✅ Selenium already installed")
        return True
    except ImportError:
        print("📦 Installing Selenium...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium", "webdriver-manager"])
            print("✅ Packages installed successfully")
            return True
        except:
            st.error("""
            ❌ Could not install Selenium automatically.
            
            Please install manually:
            ```
            pip install selenium webdriver-manager
            ```
            Then restart the app.
            """)
            return False

# Install packages before importing
if install_required_packages():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    import threading
else:
    st.stop()

# ============================================
# STREAMLIT CONFIGURATION
# ============================================

st.set_page_config(
    page_title="Facebook E2E Automation",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'facebook_driver' not in st.session_state:
    st.session_state.facebook_driver = None
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'is_sending' not in st.session_state:
    st.session_state.is_sending = False
if 'activity_log' not in st.session_state:
    st.session_state.activity_log = []

# ============================================
# REAL FACEBOOK AUTOMATION CLASS
# ============================================

class RealFacebookAutomation:
    """Real Facebook automation - End to End"""
    
    def __init__(self, headless=False):
        self.driver = None
        self.headless = headless
        self.running = True
        self.cookies_dir = Path("facebook_cookies")
        self.cookies_dir.mkdir(exist_ok=True)
    
    def setup_browser(self):
        """Setup real browser with Chrome"""
        try:
            chrome_options = Options()
            
            # Anti-detection settings
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Basic settings
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--start-maximized")
            
            if self.headless:
                chrome_options.add_argument("--headless=new")
            
            # User agent
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Setup driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Hide automation
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return True
        except Exception as e:
            st.error(f"❌ Browser setup failed: {str(e)[:200]}")
            return False
    
    def login_to_facebook(self, email, password, save_cookies=True):
        """Real Facebook login"""
        try:
            if not self.driver:
                if not self.setup_browser():
                    return False, "Browser setup failed"
            
            # Check saved cookies first
            if save_cookies:
                cookie_file = self.cookies_dir / f"{email.replace('@', '_')}.pkl"
                if cookie_file.exists():
                    self.driver.get("https://facebook.com")
                    time.sleep(2)
                    
                    try:
                        with open(cookie_file, 'rb') as f:
                            cookies = pickle.load(f)
                        
                        for cookie in cookies:
                            try:
                                self.driver.add_cookie(cookie)
                            except:
                                pass
                        
                        self.driver.refresh()
                        time.sleep(3)
                        
                        if "login" not in self.driver.current_url.lower():
                            st.session_state.activity_log.append("✅ Logged in with saved cookies")
                            return True, "Logged in with saved cookies"
                    except:
                        pass
            
            # Manual login
            self.driver.get("https://facebook.com/login")
            time.sleep(3)
            
            # Enter email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_field.send_keys(email)
            time.sleep(1)
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "pass")
            password_field.send_keys(password)
            time.sleep(1)
            
            # Click login
            login_button = self.driver.find_element(By.NAME, "login")
            login_button.click()
            time.sleep(5)
            
            # Check for 2FA
            try:
                code_field = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "approvals_code"))
                )
                return False, "2FA_REQUIRED"
            except:
                pass
            
            # Check login success
            current_url = self.driver.current_url.lower()
            if "facebook.com" in current_url and "login" not in current_url:
                # Save cookies
                if save_cookies:
                    cookies = self.driver.get_cookies()
                    with open(cookie_file, 'wb') as f:
                        pickle.dump(cookies, f)
                
                st.session_state.activity_log.append("✅ Login successful")
                return True, "Login successful"
            else:
                return False, "Login failed - check credentials"
                
        except Exception as e:
            return False, f"Login error: {str(e)[:100]}"
    
    def send_real_message(self, chat_url, message, delay=5, repeat=1):
        """Send real message to Facebook"""
        try:
            if not self.driver:
                return False, "Not logged in"
            
            self.driver.get(chat_url)
            time.sleep(5)
            
            # Find message input
            input_selectors = [
                "div[contenteditable='true'][role='textbox']",
                "div[aria-label='Message']",
                "div[data-editor='true']",
                "div[contenteditable='true']"
            ]
            
            msg_input = None
            for selector in input_selectors:
                try:
                    msg_input = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if not msg_input:
                return False, "Could not find message input"
            
            # Send messages
            for i in range(repeat):
                if not self.running:
                    break
                
                # Focus and clear
                msg_input.click()
                time.sleep(0.5)
                
                msg_input.send_keys(Keys.CONTROL + "a")
                msg_input.send_keys(Keys.DELETE)
                time.sleep(0.3)
                
                # Type with human-like delay
                for char in message:
                    msg_input.send_keys(char)
                    time.sleep(random.uniform(0.02, 0.06))
                
                # Send
                msg_input.send_keys(Keys.ENTER)
                
                # Log activity
                log_msg = f"✅ Message {i+1}/{repeat} sent to {chat_url[:30]}..."
                st.session_state.activity_log.append(log_msg)
                
                # Wait before next
                if i < repeat - 1:
                    actual_delay = delay + random.uniform(-1, 1)
                    time.sleep(max(3, actual_delay))
            
            return True, f"Sent {repeat} messages successfully"
            
        except Exception as e:
            return False, f"Error: {str(e)[:100]}"
    
    def logout(self):
        """Logout from Facebook"""
        try:
            if self.driver:
                self.driver.get("https://facebook.com/logout")
                time.sleep(3)
        except:
            pass
    
    def close(self):
        """Close browser"""
        self.running = False
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass

# ============================================
# STREAMLIT UI - REAL WORKING
# ============================================

def main():
    """Main application"""
    
    # Header
    st.title("✅ Facebook End-to-End Automation")
    st.markdown("**Real working - Login → Send Messages**")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Control Panel")
        
        if st.session_state.logged_in:
            st.success(f"✅ Logged in")
            st.caption(f"User: {st.session_state.current_user}")
            
            col_sb1, col_sb2 = st.columns(2)
            with col_sb1:
                if st.button("🔄 Refresh", use_container_width=True):
                    st.rerun()
            with col_sb2:
                if st.button("🚪 Logout", type="secondary", use_container_width=True):
                    if st.session_state.facebook_driver:
                        st.session_state.facebook_driver.logout()
                        st.session_state.facebook_driver.close()
                    st.session_state.logged_in = False
                    st.session_state.current_user = None
                    st.session_state.facebook_driver = None
                    st.rerun()
        else:
            st.warning("🔒 Not logged in")
        
        st.markdown("---")
        
        # Settings
        st.subheader("🎛️ Settings")
        headless_mode = st.checkbox("Headless Mode", value=False)
        save_cookies = st.checkbox("Save Login Cookies", value=True)
        
        st.markdown("---")
        
        # Quick stats
        st.subheader("📊 Quick Stats")
        if st.session_state.activity_log:
            total = len(st.session_state.activity_log)
            success = len([log for log in st.session_state.activity_log if "✅" in log])
            st.metric("Total Actions", total)
            st.metric("Successful", success)
        
        st.markdown("---")
        st.info("""
        **Real Features:**
        - Actual Facebook login
        - Real message sending
        - Cookie saving
        - End-to-end working
        """)
    
    # Main content
    if not st.session_state.logged_in:
        show_login_section(headless_mode, save_cookies)
    else:
        show_messaging_section()

def show_login_section(headless_mode, save_cookies):
    """Show login interface"""
    st.subheader("🔐 Real Facebook Login")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("real_login_form"):
            email = st.text_input("📧 Real Facebook Email", placeholder="your_real_email@facebook.com")
            password = st.text_input("🔑 Password", type="password", placeholder="Your real password")
            
            login_btn = st.form_submit_button("🚀 Login to Real Facebook", use_container_width=True)
            
            if login_btn:
                if not email or not password:
                    st.error("Please enter email and password")
                    return
                
                with st.spinner("Logging in to REAL Facebook..."):
                    # Create automation instance
                    automator = RealFacebookAutomation(headless=headless_mode)
                    
                    # Attempt login
                    success, message = automator.login_to_facebook(email, password, save_cookies)
                    
                    if success:
                        st.session_state.facebook_driver = automator
                        st.session_state.logged_in = True
                        st.session_state.current_user = email
                        st.success("✅ REAL Login successful!")
                        time.sleep(2)
                        st.rerun()
                    elif "2FA" in message:
                        st.warning("🔐 2FA detected! Please check browser for verification.")
                        st.info("Complete 2FA in the browser window, then click Continue.")
                        
                        if st.button("Continue after 2FA"):
                            st.session_state.facebook_driver = automator
                            st.session_state.logged_in = True
                            st.session_state.current_user = email
                            st.success("✅ Login successful after 2FA!")
                            time.sleep(2)
                            st.rerun()
                    else:
                        st.error(f"❌ {message}")
                        automator.close()
    
    with col2:
        st.subheader("⚠️ Important")
        st.info("""
        **This is REAL automation:**
        - Uses your real Facebook account
        - Actually sends messages
        - Real browser automation
        - Requires Chrome installed
        
        **Test first with:**
        - Dummy Facebook account
        - 1-2 test messages
        - Your own chat
        """)
        
        # Quick test credentials
        with st.expander("🧪 For Testing"):
            st.code("""
Use your own Facebook account
OR create test account:
1. Go to facebook.com
2. Create new account
3. Add profile picture
4. Add 1-2 friends
5. Use for testing
            """)

def show_messaging_section():
    """Show messaging interface"""
    st.subheader(f"💬 Ready to send - {st.session_state.current_user}")
    
    # Quick controls
    col_controls = st.columns(4)
    with col_controls[0]:
        if st.button("📸 Take Screenshot"):
            if st.session_state.facebook_driver and st.session_state.facebook_driver.driver:
                try:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"screenshot_{timestamp}.png"
                    st.session_state.facebook_driver.driver.save_screenshot(filename)
                    st.success(f"Screenshot saved: {filename}")
                except:
                    pass
    
    with col_controls[3]:
        if st.button("🔄 Open Facebook"):
            if st.session_state.facebook_driver and st.session_state.facebook_driver.driver:
                st.session_state.facebook_driver.driver.get("https://facebook.com")
                st.info("Facebook opened in browser")
    
    st.markdown("---")
    
    # Message configuration
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # Step 1: Chat URL
        st.markdown("#### 🔗 Step 1: Get REAL Chat URL")
        st.info("Open Facebook Messenger in browser, copy URL from address bar")
        
        chat_url = st.text_input(
            "Paste REAL Facebook Chat URL:",
            placeholder="https://www.facebook.com/messages/t/...",
            key="real_chat_url"
        )
        
        # Step 2: Message
        st.markdown("#### 📝 Step 2: Type REAL Message")
        message = st.text_area(
            "Type your REAL message:",
            height=150,
            placeholder="This will be sent for REAL...",
            key="real_message"
        )
        
        # Add variations
        if st.checkbox("Add message variation"):
            variations = ["How are you?", "Good morning!", "Hope you're doing well!"]
            variation = st.selectbox("Add ending:", variations)
            message = f"{message} {variation}"
        
        # Step 3: Timing
        st.markdown("#### ⏱️ Step 3: Real Timing")
        col_time = st.columns(2)
        with col_time[0]:
            delay = st.slider("Delay (seconds)", 3, 60, 5, help="Minimum 3 seconds recommended")
            random_delay = st.checkbox("Add random delay", value=True)
        with col_time[1]:
            repeat = st.number_input("Repeat count", 1, 20, 1, help="Start with 1-2 for testing")
    
    with col_right:
        st.markdown("#### 🎮 Step 4: Send FOR REAL")
        
        if chat_url and message:
            # Preview
            st.markdown("**REAL Preview:**")
            st.warning(f'"{message}"')
            st.caption("⚠️ This will actually be sent!")
            
            # Send button
            if st.button("🚀 SEND FOR REAL", type="primary", use_container_width=True):
                if not st.session_state.is_sending:
                    st.session_state.is_sending = True
                    
                    # Calculate delay
                    actual_delay = delay
                    if random_delay:
                        actual_delay = max(3, delay + random.uniform(-2, 2))
                    
                    # Show warning
                    st.warning("⚠️ This will ACTUALLY send messages to Facebook!")
                    confirm = st.checkbox("I understand this is REAL and not simulation")
                    
                    if confirm:
                        # Start sending in thread
                        def send_real_messages():
                            success, result = st.session_state.facebook_driver.send_real_message(
                                chat_url, message, actual_delay, repeat
                            )
                            
                            if success:
                                st.session_state.activity_log.append(f"🎉 {result}")
                            else:
                                st.session_state.activity_log.append(f"❌ {result}")
                            
                            st.session_state.is_sending = False
                        
                        thread = threading.Thread(target=send_real_messages, daemon=True)
                        thread.start()
                        
                        st.success(f"✅ Started sending {repeat} REAL messages!")
                        st.balloons()
                    else:
                        st.error("Please confirm you understand this is REAL")
                        st.session_state.is_sending = False
            else:
                st.info("Ready to send REAL messages")
            
            # Stop button
            if st.button("⏹️ STOP REAL SENDING", type="secondary", use_container_width=True):
                if st.session_state.facebook_driver:
                    st.session_state.facebook_driver.running = False
                    st.warning("⏹️ Stopping REAL message sending...")
        else:
            st.warning("Enter chat URL and message")
        
        # Quick guide
        with st.expander("📋 REAL Guide"):
            st.info("""
            **For first time:**
            1. Login with real account
            2. Test with your own chat
            3. Send 1 message first
            4. Check if received
            5. Then send more
            
            **Safety:**
            - Start with 1 message
            - Use 5+ seconds delay
            - Don't spam
            - Monitor browser window
            """)
    
    # Activity log
    st.markdown("---")
    st.subheader("📊 REAL Activity Log")
    
    if st.session_state.activity_log:
        log_container = st.container(height=300)
        with log_container:
            for log in reversed(st.session_state.activity_log[-20:]):
                if "✅" in log or "🎉" in log:
                    st.success(log)
                elif "❌" in log:
                    st.error(log)
                else:
                    st.info(log)
    else:
        st.info("No REAL activity yet")
    
    # Clear log button
    if st.button("Clear Activity Log"):
        st.session_state.activity_log = []
        st.rerun()

# ============================================
# RUN APPLICATION
# ============================================

if __name__ == "__main__":
    # Check if running on cloud
    if 'STREAMLIT_SHARING' in os.environ or 'STREAMLIT_SERVER' in os.environ:
        st.error("""
        ❌ This app requires local browser automation.
        
        **Cannot run on Streamlit Cloud/Sharing.**
        
        **Run locally instead:**
        ```
        pip install streamlit selenium webdriver-manager
        streamlit run facebook_real_e2e.py
        ```
        """)
        st.stop()
    
    main()
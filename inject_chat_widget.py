import os
import glob
import re

def inject_chat_widget():
    directory = 'c:/Xamp/htdocs/abhinaya'
    html_files = glob.glob(os.path.join(directory, '*.html'))
    php_files = glob.glob(os.path.join(directory, '*.php'))
    all_files = html_files + php_files
    
    ignore_files = [
        'config.php', 'db.php', 'setup.php', 'setup_contacts.php', 'setup_receipt.php', 
        'test.php', 'alter_table.php', 'create_table.php', 'drop_cols.php', 'send_otp.php', 
        'verify_otp.php', 'chatbot_api.php', 'ensure_payments_table.php', 'test_chatbot.php',
        'update_frontend_v2.py', 'build_fee_payment_page.py', 'create_courses_page.py', 'create_schedule_page.py'
    ]
    
    widget_file = os.path.join(directory, 'chat-widget.html')
    if not os.path.exists(widget_file):
        print(f"Error: {widget_file} not found.")
        return
        
    with open(widget_file, 'r', encoding='utf-8') as f:
        widget_code = f.read().strip()

    start_marker = '<!-- AI Chat Widget -->'
    end_marker = '<!-- End AI Chat Widget -->'
    
    wrapped_widget = f"{start_marker}\n{widget_code}\n{end_marker}"
    
    count = 0
    for file_path in all_files:
        filename = os.path.basename(file_path)
        if filename in ignore_files or filename == 'chat-widget.html' or filename.startswith('.'):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # If start marker exists, replace entire widget block
            if start_marker in content:
                if end_marker in content:
                    pattern = re.compile(re.escape(start_marker) + r'.*?' + re.escape(end_marker), re.DOTALL)
                    new_content = pattern.sub(lambda m: wrapped_widget, content)
                else:
                    pattern = re.compile(re.escape(start_marker) + r'.*?<\/script>', re.DOTALL)
                    new_content = pattern.sub(lambda m: wrapped_widget, content)
                    
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated widget in {filename}")
                    count += 1
            else:
                # Inject right before the LAST </body> in the file
                if '</body>' in content:
                    parts = content.rsplit('</body>', 1)
                    new_content = parts[0] + f'\n{wrapped_widget}\n</body>' + parts[1]
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Injected widget into {filename}")
                    count += 1
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    print(f"Successfully processed {count} files with AI Chat Widget.")

if __name__ == "__main__":
    inject_chat_widget()

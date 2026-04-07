#import flask
#from flask import Flask

#app = Flask(__name__)

#@app.route('/')
#def hello():
    #return "vanakkam da maapla chennai la irundu"

#if __name__ == '__main__':
    #app.run(debug=True)

from flask import Flask, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def scrape_hora_direct():
    with sync_playwright() as p:
        # Use a real browser header to look less like a bot
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0")
        page = context.new_page()

        try:
            # Navigate directly to a timing site (Example: DrikPanchang)
            # This is much more reliable for an API than Google Search
            page.goto("https://www.drikpanchang.com/panchang/hora-panchangam.html?location=chennai", wait_until="domcontentloaded")
            
            # Wait for the table or element containing the current Hora
            # Note: You may need to inspect the specific site to get the exact selector
            hora_element = page.locator(".dpHoraData").first # Example selector
            
            if hora_element.is_visible():
                current_hora = hora_element.inner_text()
            else:
                current_hora = "Site loaded, but Hora element not found."

            return {"status": "success", "current_hora": current_hora}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            browser.close()

@app.route('/get-hora', methods=['GET'])
def get_hora_api():
    return jsonify(scrape_hora_direct())

if __name__ == "__main__":
    app.run(debug=True, port=5000)
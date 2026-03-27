from flask import Flask, request, jsonify
from google import genai
from PIL import Image
import os
import re
import json

app = Flask(__name__)

# ✅ Load API key
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


@app.route('/')
def home():
    return "Mediscan Backend Running ✅"


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files['image']
        machine = request.form.get("machine", "Unknown")

        image = Image.open(file.stream)

        # 🎯 SMART PROMPT HANDLING
        if machine == "Fresenius 5008":
            prompt = """
Return ONLY JSON:

{
  "device_info": {
    "model": "Fresenius 5008"
  },
  "machine_parameters": {
    "Date": "",
    "Remaining Time": "",
    "UF goal": "",
    "UF rate": "",
    "UF volume": "",
    "Blood flow": "",
    "VEN": "",
    "ART": ""
  }
}
"""

        elif machine == "Fresenius 4008 S":
            prompt = """
Return ONLY JSON:

{
  "device_info": {
    "model": "Fresenius 4008 S"
  },
  "machine_parameters": {
    "Date": "",
    "Time": "",
    "UF Volume": "",
    "UF Time Left": "",
    "UF Rate": "",
    "UF Goal": "",
    "Blood Flow": "",
    "Kt/V": "",
    "Arterial Pressure": "",
    "Venous Pressure": "",
    "TMP": "",
    "Conductivity": ""
  }
}
"""

        else:
            # ✅ Generic fallback (VERY IMPORTANT)
            prompt = f"""
Extract all visible parameters from this dialysis machine screen.

Return ONLY JSON:

{{
  "device_info": {{
    "model": "{machine}"
  }},
  "machine_parameters": {{
    "Parameter 1": "",
    "Parameter 2": "",
    "Parameter 3": ""
  }}
}}
"""

        # 🚀 Gemini API call
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[prompt, image],
        )

        text = response.text.strip()
        print("RAW OUTPUT:\n", text)

        # ✅ Extract JSON safely
        match = re.search(r'\{.*\}', text, re.DOTALL)

        if not match:
            return jsonify({
                "error": "Invalid JSON from Gemini",
                "raw": text
            })

        parsed = json.loads(match.group(0))

        return jsonify({"result": parsed})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


# ✅ Required for Render
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# from flask import Flask, request, jsonify
# from google import genai
# from PIL import Image
# import os
# import re
# import json

# app = Flask(__name__)

# # 🔐 Use environment variable (IMPORTANT)
# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     try:
#         file = request.files['image']
#         machine = request.form.get("machine", "default")

#         image = Image.open(file.stream)

#         # 🎯 MACHINE-SPECIFIC PROMPTS (UPDATED STRUCTURE)

#         if machine == "Fresenius 5008":
#             prompt = """
# Extract data from dialysis machine screen.

# Return STRICT JSON:

# {
#   "device_info": {
#     "model": "Fresenius 5008"
#   },
#   "machine_parameters": {
#     "Date": "",
#     "Remaining Time": "",
#     "UF goal": "",
#     "UF rate": "",
#     "UF volume": "",
#     "Blood flow": "",
#     "VEN": "",
#     "ART": ""
#   }
# }
# """

#         elif machine == "Fresenius 4008 S":
#             prompt = """
# Extract data from dialysis machine screen.

# Return STRICT JSON:

# {
#   "device_info": {
#     "model": "Fresenius 4008 S"
#   },
#   "machine_parameters": {
#     "Date": "",
#     "Time": "",
#     "UF Volume": "",
#     "UF Time Left": "",
#     "UF Rate": "",
#     "UF Goal": "",
#     "Blood Flow": "",
#     "Kt/V": "",
#     "Arterial Pressure": "",
#     "Venous Pressure": "",
#     "TMP": "",
#     "Conductivity": ""
#   }
# }
# """

#         else:
#             prompt = """
# Extract all visible data.

# Return STRICT JSON:

# {
#   "device_info": {
#     "model": "Unknown"
#   },
#   "machine_parameters": {}
# }
# """

#         # 🚀 Gemini call (FIXED ORDER + FASTER MODEL)
#         response = client.models.generate_content(
#             model="gemini-1.5-flash",
#             contents=[prompt, image]
#         )

#         text = response.text
#         print("RAW GEMINI OUTPUT:\n", text)

#         # ✅ SAFE JSON extraction
#         match = re.search(r'\{.*\}', text, re.DOTALL)

#         if match:
#             parsed = json.loads(match.group(0))

#             return jsonify({
#                 "result": parsed
#             })
#         else:
#             return jsonify({
#                 "error": "Invalid JSON from Gemini",
#                 "raw": text
#             })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)


# 🔐 Use environment variable (IMPORTANT)
# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     try:
#         file = request.files['image']
#         machine = request.form.get("machine", "default")

#         image = Image.open(file.stream)

#         # 🎯 MACHINE-SPECIFIC PROMPTS
#         if machine == "Fresenius 5008":
#             prompt = """
# Extract medical parameters from this dialysis machine screen.

# Return ONLY JSON:
# {
#   "Date": "",
#   "Remaining Time": "",
#   "UF goal": "",
#   "UF rate": "",
#   "UF volume": "",
#   "Blood flow": "",
#   "VEN": "",
#   "ART": ""
# }
# """
#         elif machine == "Fresenius 4008 S":
#             prompt = """
# Extract medical parameters from this dialysis machine screen.

# Return ONLY JSON:
# {
#   "Date": "",
#   "Time": "",
#   "UF Volume": "",
#   "UF Time Left": "",
#   "UF Rate": "",
#   "UF Goal": "",
#   "Blood Flow": "",
#   "Kt/V": "",
#   "Arterial Pressure": "",
#   "Venous Pressure": "",
#   "TMP": "",
#   "Conductivity": ""
# }
# """
#         else:
#             prompt = "Extract all visible data and return JSON only."

#         # 🚀 Gemini call
#         response = client.models.generate_content(
#             model="gemini-3-flash-preview",
#             contents=[image, prompt]
#         )

#         text = response.text
#         print("RAW GEMINI OUTPUT:\n", text)

#         # ✅ SAFE JSON extraction
#         match = re.search(r'\{.*\}', text, re.DOTALL)

#         if match:
#             parsed = json.loads(match.group(0))
#             return jsonify({"result": parsed})
#         else:
#             return jsonify({
#                 "error": "Invalid JSON from Gemini",
#                 "raw": text
#             })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# # ✅ IMPORTANT for Render deployment
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

# from flask import Flask, request, jsonify
# import os
# from img_scraping import getString

# app = Flask(__name__)

# UPLOAD_FOLDER = "uploads"
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# @app.route("/extract", methods=["POST"])
# def extract():
#     try:
#         # 📥 Get machine name
#         machine = request.form.get("machine")

#         # 📥 Get image file
#         file = request.files.get("image")

#         if not file:
#             return jsonify({"error": "No image received"}), 400

#         # 📁 Save image
#         image_path = os.path.join(UPLOAD_FOLDER, file.filename)
#         file.save(image_path)

#         print("📷 Image received:", image_path)
#         print("⚙️ Machine:", machine)

#         # 🔥 Call your Python function
#         result = getString(None, image_path, machine)

#         print("✅ Result:", result)

#         return jsonify({"result": result})

#     except Exception as e:
#         print("❌ ERROR:", str(e))
#         return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)

# from flask import Flask, request, jsonify
# import os
# from img_scraping import getString

# app = Flask(__name__)

# UPLOAD_FOLDER = "uploads"
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# @app.route("/extract", methods=["POST"])
# def extract():
#     try:
#         # 📥 Get machine name
#         machine = request.form.get("machine")

#         # 📥 Get image file
#         file = request.files.get("image")

#         if not file:
#             return jsonify({"error": "No image received"}), 400

#         # 📁 Save image
#         image_path = os.path.join(UPLOAD_FOLDER, file.filename)
#         file.save(image_path)

#         print("📷 Image received:", image_path)
#         print("⚙️ Machine:", machine)

#         # 🔥 Call your Python function
#         result = getString(None, image_path, machine)

#         print("✅ Result:", result)

#         return jsonify({"result": result})

#     except Exception as e:
#         print("❌ ERROR:", str(e))
#         return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# from datetime import datetime
# import sys

# sys.stdout.reconfigure(encoding='utf-8')

# from img_scraping import getString

# app = Flask(__name__)
# CORS(app)

# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# @app.route("/", methods=["GET"])
# def home():
#     return "Server is running"


# @app.route("/extract", methods=["POST"])
# def extract():
#     try:
#         print("\n===== NEW REQUEST =====")

#         if 'image' not in request.files:
#             return jsonify({"error": "No image key in request"}), 400

#         image = request.files['image']
#         machine = request.form.get("machine")

#         print("Machine:", machine)

#         if not machine:
#             return jsonify({"error": "Machine not provided"}), 400

#         if image.filename == "":
#             return jsonify({"error": "Empty image file"}), 400

#         filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
#         image_path = os.path.join(UPLOAD_FOLDER, filename)
#         image.save(image_path)

#         print("Image saved:", image_path)
#         print("Calling Gemini...")

#         ref_img_path = None
#         if machine == "Fresenius 4008 S":
#             ref_img_path = "ref_images/fresenius_4008.jpg"

#             if not os.path.exists(ref_img_path):
#                 return jsonify({"error": "Reference image missing"}), 500

#         # ✅ FIXED
#         result = getString(
#             ref_img=ref_img_path,
#             image_path=image_path,
#             machineName=machine
#         )

#         print("Gemini finished")
#         print("Final Result:", result)

#         # cleanup
#         try:
#             if os.path.exists(image_path):
#                 os.remove(image_path)
#         except Exception as e:
#             print("File delete error:", e)

#         if result is None:
#             result = {"error": "No data extracted"}

#         return jsonify({
#             "status": "success",
#             "result": result
#         })

#     except Exception as e:
#         print("ERROR:", str(e))
#         return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     print("Starting Flask server...")
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# from datetime import datetime
# import sys

# # Fix Windows encoding issue
# sys.stdout.reconfigure(encoding='utf-8')

# # ✅ IMPORT CORRECT FILE + FUNCTION
# # from img_scraping import extract_dialysis_parameters
# from img_scraping import getString

# app = Flask(__name__)
# CORS(app)

# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# @app.route("/", methods=["GET"])
# def home():
#     return "Server is running"


# @app.route("/extract", methods=["POST"])
# def extract():
#     try:
#         print("\n===== NEW REQUEST =====")

#         # ✅ Check image key
#         if 'image' not in request.files:
#             return jsonify({"error": "No image key in request"}), 400

#         image = request.files['image']
#         machine = request.form.get("machine")

#         print("Machine:", machine)

#         # ✅ Validate inputs
#         if not machine:
#             return jsonify({"error": "Machine not provided"}), 400

#         if image.filename == "":
#             return jsonify({"error": "Empty image file"}), 400

#         # ✅ Save image temporarily
#         filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
#         image_path = os.path.join(UPLOAD_FOLDER, filename)
#         image.save(image_path)

#         print("Image saved:", image_path)
#         print("Calling Gemini...")

#         # ✅ Handle reference image (only for Fresenius 4008 S)
#         ref_img_path = None
#         if machine == "Fresenius 4008 S":
#             ref_img_path = "ref_images/fresenius_4008.jpg"

#             if not os.path.exists(ref_img_path):
#                 return jsonify({"error": "Reference image missing"}), 500

#         # ✅ Call your main Python function
#         # result = extract_dialysis_parameters(
#         #     ref_img=ref_img_path,
#         #     image_path=image_path,
#         #     machineName=machine
#         # )

#         result = getString(
#              ref_img=ref_img_path,
#              image_path=image_path,
#              machineName=machine
#         )

#         print("Gemini finished")
#         print("Final Result:", result)

#         # ✅ Delete temp image (IMPORTANT)
#         if os.path.exists(image_path):
#             os.remove(image_path)

#         # ✅ Handle empty result
#         if result is None:
#             return jsonify({"error": "Extraction failed"}), 500

#         return jsonify({
#             "status": "success",
#             "result": result
#         })

#     except Exception as e:
#         print("ERROR:", str(e))
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     print("Starting Flask server...")
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)

# if __name__ == "__main__":
#     print("Starting Flask server...")
#     app.run(host="0.0.0.0", port=5000)

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# from datetime import datetime
# import sys

# # Fix Windows encoding issue
# sys.stdout.reconfigure(encoding='utf-8')

# from dialysis import dialysis_get_string

# app = Flask(__name__)
# CORS(app)

# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route("/", methods=["GET"])
# def home():
#     return "Server is running"


# @app.route("/extract", methods=["POST"])
# def extract():
#     try:
#         print("\n===== NEW REQUEST =====")

#         # Check request
#         if 'image' not in request.files:
#             print("No image key in request")
#             return jsonify({"error": "No image key"}), 400

#         image = request.files['image']
#         machine = request.form.get("machine")

#         print("Machine:", machine)

#         if image.filename == "":
#             print("Empty image file")
#             return jsonify({"error": "Empty image"}), 400

#         # Save image
#         filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
#         image_path = os.path.join(UPLOAD_FOLDER, filename)
#         image.save(image_path)

#         print("Image saved:", image_path)

#         print("Calling Gemini...")

#         # ✅ Handle ref image only for Fresenius 4008
#         if machine == "Fresenius 4008 S":
#             ref_img_path = "ref_images/fresenius_4008.jpg"
#         else:
#             ref_img_path = None

#         result = dialysis_get_string(
#             ref_img=ref_img_path,
#             image_path=image_path,
#             machineName=machine
#         )

#         print("Gemini finished")
#         print("Final Result:", result)

#         return jsonify({
#             "status": "success",
#             "result": result
#         })

#     except Exception as e:
#         print("ERROR:", str(e))
#         return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     print("Starting Flask server...")
#     app.run(host="0.0.0.0", port=5000, debug=True)








# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# from datetime import datetime
# import sys

# # ✅ Fix Windows encoding issue (VERY IMPORTANT)
# sys.stdout.reconfigure(encoding='utf-8')

# from dialysis import dialysis_get_string

# app = Flask(__name__)
# CORS(app)

# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # ✅ Test route
# @app.route("/", methods=["GET"])
# def home():
#     return "Server is running"

# print("EXTRACT API HIT")

# @app.route("/extract", methods=["POST"])
# def extract():
#     try:
#         print("\n===== NEW REQUEST =====")

#         # Check request
#         if 'image' not in request.files:
#             print("No image key in request")
#             return jsonify({"error": "No image key"}), 400

#         image = request.files['image']
#         machine = request.form.get("machine")

#         print("Machine:", machine)

#         if image.filename == "":
#             print("Empty image file")
#             return jsonify({"error": "Empty image"}), 400

#         # Save image
#         filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
#         image_path = os.path.join(UPLOAD_FOLDER, filename)
#         image.save(image_path)

#         print("Image saved:", image_path)

#         print("Calling Gemini...")

#         # ✅ FIXED BLOCK (INSIDE FUNCTION)
#         if machine == "Fresenius 4008 S":
#             ref_img_path = "ref_images/fresenius_4008.jpg"

#             result = dialysis_get_string(
#                 ref_img=ref_img_path,
#                 image_path=image_path,
#                 machineName=machine
#             )
#         else:
#             result = dialysis_get_string(
#                 ref_img=None,
#                 image_path=image_path,
#                 machineName=machine
#             )

#         print("Gemini finished")
#         print("Final Result:", result)

#         return jsonify({
#             "status": "success",
#             "result": result
#         })

#     except Exception as e:
#         print("ERROR:", str(e))
#         return jsonify({"error": str(e)}), 500
    
# if __name__ == "__main__":
#     print("Starting Flask server...")
#     app.run(host="0.0.0.0", port=5000, debug=True)


































# @app.route("/extract", methods=["POST"])
# def extract():
#     try:
#         print("\n===== NEW REQUEST =====")

#         # 🔹 Check incoming request
#         if 'image' not in request.files:
#             print("No image key in request")
#             return jsonify({"error": "No image key"}), 400

#         image = request.files['image']
#         machine = request.form.get("machine")

#         print("Machine:", machine)

#         if image.filename == "":
#             print("Empty image file")
#             return jsonify({"error": "Empty image"}), 400

#         # 🔹 Save image
#         filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
#         image_path = os.path.join(UPLOAD_FOLDER, filename)
#         image.save(image_path)

#         print("Image saved:", image_path)

#         # 🔥 DEBUG BEFORE GEMINI
#         print("Calling Gemini...")

#         # result = dialysis_get_string(
#         #     image_path=image_path,
#         #     machineName=machine
#         # )

# if machine == "Fresenius 4008 S":
#     ref_img_path = "ref_images/fresenius_4008.jpg"

#     result = dialysis_get_string(
#         ref_img=ref_img_path,
#         image_path=image_path,
#         machineName=machine
#     )
# else:
#     result = dialysis_get_string(
#         ref_img=None,
#         image_path=image_path,
#         machineName=machine
#     )

# # 🔥 DEBUG AFTER GEMINI
# print("Gemini finished")

# print("Final Result:", result)

# return jsonify({
#     "status": "success",
#     "result": result
# })

#     except Exception as e:
#         print("ERROR:", str(e))
#         return jsonify({"error": str(e)}), 500



# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# from datetime import datetime

# from dialysis import dialysis_get_string

# app = Flask(__name__)
# CORS(app)

# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # ✅ Test route
# @app.route("/", methods=["GET"])
# def home():
#     return "Server is running"


# @app.route("/extract", methods=["POST"])
# def extract():
#     try:
#         print("\n===== NEW REQUEST =====")

#         image = request.files.get("image")
#         machine = request.form.get("machine")

#         print("Machine:", machine)

#         if not image:
#             print(" No image received")
#             return jsonify({"error": "No image"}), 400

#         filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
#         image_path = os.path.join(UPLOAD_FOLDER, filename)
#         image.save(image_path)

#         print(" Image saved:", image_path)

#         result = dialysis_get_string(
#             image_path=image_path,
#             machineName=machine
#         )

#         print(" Final Result:", result)

#         return jsonify({
#             "status": "success",
#             "result": result
#         })

#     except Exception as e:
#         print(" ERROR:", str(e))
#         return jsonify({"error": str(e)}), 500
    
    
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)



# ✅ Main API
# @app.route("/extract", methods=["POST"])
# def extract():
#     try:
#         print("\n===== NEW REQUEST =====")

#         image = request.files.get("image")
#         machine = request.form.get("machine")

#         print("Machine:", machine)

#         if not image:
#             return jsonify({"error": "No image"}), 400

#         # Save image
#         filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
#         image_path = os.path.join(UPLOAD_FOLDER, filename)
#         image.save(image_path)

#         print("Image saved:", image_path)

#         # ✅ CALL GEMINI FUNCTION
#         result = dialysis_get_string(
#             image_path=image_path,
#             machineName=machine
#         )

#         print("Result:", result)

#         return jsonify({
#             "status": "success",
#             "machine": machine,
#             "result": result
#         })

#     except Exception as e:
#         print("ERROR:", str(e))
#         return jsonify({"error": str(e)}), 500




# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# from datetime import datetime

# from dialysis import dialysis_get_string

# # ✅ Create app FIRST
# app = Flask(__name__)
# CORS(app)

# # ✅ Folder setup
# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # ✅ Home route
# @app.route("/", methods=["GET"])
# def home():
#     return "Server is running"

# # ✅ Main API
# @app.route("/extract", methods=["POST"])
# def extract():
#     try:
#         print("\n===== NEW REQUEST =====")

#         image = request.files.get("image")
#         machine = request.form.get("machine")

#         print("Machine:", machine)

#         if not image:
#             print("No image received")
#             return jsonify({"error": "No image"}), 400

#         filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
#         image_path = os.path.join(UPLOAD_FOLDER, filename)

#         image.save(image_path)
#         print("Image saved at:", image_path)

#         result = dialysis_get_string(
#             ref_img=None,
#             image_path=image_path,
#             machineName=machine,
#             # gemini_endpoint="https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
#             gemini_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent",
#             api_key="AIzaSyBH8zBxdmx337NWhbpJzhjR2BSOQk35IKk"
#         )

#         print("Result:", result)

#         return jsonify({
#             "status": "success",
#             "machine": machine,
#             "result": result
#         })

#     except Exception as e:
#         print("ERROR:", str(e))
#         return jsonify({"error": str(e)}), 500

# # ✅ Run server LAST
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)










# from flask import Flask, request, jsonify
# from flask_cors import CORS  # ✅ ADD THIS
# import os
# from datetime import datetime

# from dialysis import dialysis_get_string

# app = Flask(__name__)

# CORS(app, resources={r"/*": {"origins": "*"}})


# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', '*')
#     response.headers.add('Access-Control-Allow-Methods', '*')
#     return response

# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# # from flask import Flask, request, jsonify
# # import os
# # from datetime import datetime

# # from dialysis import dialysis_get_string

# # app = Flask(__name__)
# # CORS(app)

# # # 📁 Folder to store uploaded images
# # UPLOAD_FOLDER = "uploads"
# # os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# # # ✅ Test route (VERY useful)
# @app.route("/", methods=["GET"])
# def home():
#     return "✅ Server is running"


# # # ✅ Main API
# @app.route("/extract", methods=["POST"])
# def extract():
#     try:
#         print("\n📥 ===== NEW REQUEST =====")

#         # 📷 Get data
#         image = request.files.get("image")
#         machine = request.form.get("machine")

#         print("📌 Machine:", machine)

#         if not image:
#             print("❌ No image received")
#             return jsonify({"error": "No image"}), 400

#         # 🕒 Unique filename (avoid overwrite)
#         filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
#         image_path = os.path.join(UPLOAD_FOLDER, filename)

#         # 💾 Save image
#         image.save(image_path)
#         print("💾 Image saved at:", image_path)

#         # 🤖 Call your extraction logic
#         result = dialysis_get_string(
#             ref_img=None,
#             image_path=image_path,
#             machineName=machine,
#             gemini_endpoint="https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent",
#             api_key="AIzaSyBH8zBxdmx337NWhbpJzhjR2BSOQk35IKk"
#         )

#         print("📊 Result:", result)

#         return jsonify({
#             "status": "success",
#             "machine": machine,
#             "result": result
#         })

#     except Exception as e:
#         print("🔥 ERROR:", str(e))
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500


# # 🚀 Run server
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)













# # from flask import Flask, request, jsonify
# # import os

# # from dialysis import dialysis_get_string


# # # gemini-api - AIzaSyBH8zBxdmx337NWhbpJzhjR2BSOQk35IKk


# # app = Flask(__name__)

# # UPLOAD_FOLDER = "uploads"
# # os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # @app.route("/extract", methods=["POST"])
# # def extract():
# #     try:
# #         print("Request received")

# #         image = request.files.get("image")
# #         machine = request.form.get("machine")

# #         print("Machine:", machine)

# #         if not image:
# #             return jsonify({"error": "No image"}), 400

# #         image_path = os.path.join(UPLOAD_FOLDER, image.filename)
# #         image.save(image_path)

# #         print("Image saved at:", image_path)

# #         result = dialysis_get_string(
# #             ref_img=None,
# #             image_path=image_path,
# #             machineName=machine,
# #             gemini_endpoint="https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent",
# #             api_key="AIzaSyBH8zBxdmx337NWhbpJzhjR2BSOQk35IKk"
# #         )

# #         print("Result:", result)

# #         return jsonify(result)

# #     except Exception as e:
# #         print("ERROR:", str(e))
# #         return jsonify({"error": str(e)}), 500
    
# # if __name__ == "__main__":
# #     app.run(host="0.0.0.0", port=5000)

# # @app.route("/extract", methods=["POST"])
# # def extract():
# #     try:
# #         image = request.files.get("image")
# #         machine = request.form.get("machine")

# #         if not image:
# #             return jsonify({"error": "No image"}), 400

# #         # 👉 save image
# #         image_path = os.path.join(UPLOAD_FOLDER, image.filename)
# #         image.save(image_path)

# #         print("Machine:", machine)

# #         # 👉 call YOUR function
# #         result = dialysis_get_string(
# #             ref_img=None,   # or pass if needed
# #             image_path=image_path,
# #             machineName=machine,
# #             gemini_endpoint="YOUR_ENDPOINT",
# #             api_key="AIzaSyBH8zBxdmx337NWhbpJzhjR2BSOQk35IKk"
# #         )

# #         return jsonify(result)

# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500


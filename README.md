# 🏎️ Velocity Labs | Car Performance Hub

**Velocity Labs** is a high-end web platform designed for Car enthusiasts to explore performance parts and manage their automotive profile. The site features a cinematic user experience with integrated video backgrounds and a secure administrative backend.

## 🚀 Key Features
* **Cinematic UI:** High-definition Car video backgrounds for an immersive experience.
* **Secure Authentication:** Custom-built login and signup system using JSON-based data storage.
* **Admin Shield:** Environment-variable protected administrative access to secure the project's "Engine."
* **Responsive Design:** Optimized for high-performance browsing.

## 🛠️ Technical Stack
* **Backend:** Python 3 with the **Flask** framework.
* **Production Server:** **Waitress** (WSGI) for stable, high-concurrency deployment.
* **Frontend:** HTML5, CSS3, and JavaScript.
* **Deployment:** Integrated via **GitHub** and hosted on **Render**.

## 📂 Project Structure
* `app.py`: The heart of the application handling routing and security.
* `static/`: Contains the "garage" of the site—all BMW videos, images, and CSS.
* `templates/`: The visual blueprints of the site (HTML files).
* `requirements.txt`: Lists the essential Python libraries for the engine.
* `users.json`: The local database for user profile management.

## 🔐 Installation & Security
To run this project locally, ensure you set the environment variables in your terminal to protect the admin credentials:

```powershell
# Set local security keys
$env:ADMIN_USER = "admin"
$env:ADMIN_PASS = "velocity2026"

# Start the engine
python app.py

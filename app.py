from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    budget = db.Column(db.Float, nullable=False, default=1000.0)  # Default budget
    transactions = db.relationship('Transaction', backref='user', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)  # income or expense
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        flash('Invalid credentials. Please try again.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)
    transactions = Transaction.query.filter_by(user_id=user_id).all()

    # Separate income and expense transactions
    income = sum(t.amount for t in transactions if t.transaction_type == 'income')
    expenses = sum(t.amount for t in transactions if t.transaction_type == 'expense')

    # Budget Analysis
    budget_left = user.budget - expenses

    # Spending by category
    categories = {}
    for transaction in transactions:
        if transaction.transaction_type == 'expense':
            if transaction.category in categories:
                categories[transaction.category] += transaction.amount
            else:
                categories[transaction.category] = transaction.amount

    # Spending breakdown in percentages
    total_expenses = sum(categories.values())
    category_percentages = {k: (v / total_expenses) * 100 for k, v in categories.items()} if total_expenses > 0 else {}

    # Recommendations based on spending patterns
    recommendations = []
    if expenses > income:
        recommendations.append("You're spending more than you're earning. Consider cutting down on discretionary spending.")
    if total_expenses > user.budget:
        recommendations.append("You're exceeding your monthly budget. Try to reduce spending in categories like dining or entertainment.")
    if 'Entertainment' in categories and categories['Entertainment'] > 0.2 * total_expenses:
        recommendations.append("You're spending a significant amount on entertainment. Consider setting a limit for entertainment spending.")

    # Visualization
    plt.figure(figsize=(10, 5))
    plt.bar(categories.keys(), categories.values(), color='blue')
    plt.xlabel('Categories')
    plt.ylabel('Amount')
    plt.title('Expenses by Category')

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('dashboard.html', 
                           transactions=transactions, 
                           plot_url=plot_url,
                           income=income, 
                           expenses=expenses, 
                           budget_left=budget_left, 
                           category_percentages=category_percentages,
                           recommendations=recommendations)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    amount = float(request.form['amount'])
    category = request.form['category']
    transaction_type = request.form['transaction_type']

    new_transaction = Transaction(amount=amount, category=category, transaction_type=transaction_type, user_id=user_id)
    db.session.add(new_transaction)
    db.session.commit()
    
    return redirect(url_for('dashboard'))

@app.route('/set_budget', methods=['POST'])
def set_budget():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    new_budget = float(request.form['budget'])
    user.budget = new_budget
    db.session.commit()
    
    flash('Budget updated successfully!')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)


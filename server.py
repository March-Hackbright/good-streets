from flask import Flask, render_template, session, flash, redirect, request, jsonify

app = Flask(__name__)
app.secret_key="Best Hackbright Team"

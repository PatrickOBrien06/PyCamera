from website import create_app

# Run main file
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0")
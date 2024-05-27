from app import creat_app
app =creat_app()
if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)


# tree -I "node_modules|cache|test_*"
# tree -I "__pycache__"
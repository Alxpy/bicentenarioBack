
def get_email_send_code_html(code):
    return f"""
        <!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Verificación de Código</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: #f3f4f6;
            font-family: Arial, sans-serif;
        }}
        .contenedor {{
            width: 100%;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .card {{
            width: 100%;
            max-width: 400px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
            padding: 20px;
        }}
        .card-header {{
            background-color: #334155;
            color: #fff;
            font-size: 18px;
            font-weight: bold;
            padding: 15px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }}
        .card-body {{
            padding: 20px;
        }}
        .card-footer {{
            background-color: #334155;
            color: #fff;
            padding: 10px;
            font-size: 14px;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        }}
        .codigo {{
            font-size: 28px;
            font-weight: bold;
            color: #fff;
            background-color: #fb923c;
            padding: 15px 30px;
            border-radius: 8px;
            display: inline-block;
            margin-top: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            letter-spacing: 2px;
        }}
        p {{
            font-size: 16px;
            color: #4b5563;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="contenedor">
        <div class="card">
            <div class="card-header">
                Bienvenido a Sistema Bicentenario
            </div>
            <div class="card-body">
                <h2>Código de Verificación</h2>
                <p>Usa este código para verificar tu cuenta:</p>
                <div class="codigo">{code}</div>
                <p>Si no solicitaste este código, puedes ignorar este mensaje.</p>
            </div>
            <div class="card-footer">
                alxpy
            </div>
        </div>
    </div>
</body>
</html>

        """


def get_email_send_verify_html(code):
    return f"""
        <!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Verificación de Correo</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: #f3f4f6;
            font-family: Arial, sans-serif;
        }}
        .contenedor {{
            width: 100%;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .card {{
            width: 100%;
            max-width: 400px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
            padding: 20px;
        }}
        .card-header {{
            background-color: #334155;
            color: #fff;
            font-size: 18px;
            font-weight: bold;
            padding: 15px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }}
        .card-body {{
            padding: 20px;
        }}
        .card-footer {{
            background-color: #334155;
            color: #fff;
            padding: 10px;
            font-size: 14px;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        }}
        .codigo {{
            font-size: 28px;
            font-weight: bold;
            color: #fff;
            background-color: #fb923c;
            padding: 15px 30px;
            border-radius: 8px;
            display: inline-block;
            margin-top: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            letter-spacing: 2px;
        }}
        p {{
            font-size: 16px;
            color: #4b5563;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="contenedor">
        <div class="card">
            <div class="card-header">
                Bienvenido a Sistema Bicentenario
            </div>
            <div class="card-body">
                <h2>Código de Verificación</h2>
                <p>Usa este código para verificar tu cuenta:</p>
                <div class="codigo">{code}</div>
                <p>Si no solicitaste este código, puedes ignorar este mensaje.</p>
            </div>
            <div class="card-footer">
                alxpy
            </div>
        </div>
    </div>
</body>
</html>

        """

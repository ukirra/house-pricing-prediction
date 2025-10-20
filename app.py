import os

import joblib
import numpy as np
import pandas as pd
from flask import (Flask, flash, make_response, redirect, render_template,
                   request, session, url_for)

FEATURES = ["LB", "LT", "KT", "KM", "GRS"]
MODEL_PATH = os.path.join("model", "model.joblib")
LOG_TARGET = True

app = Flask(__name__)
app.secret_key = "dev-key"
model = joblib.load(MODEL_PATH)


def rupiah(x: float) -> str:
    try:
        v = int(round(x, -3))
        return f"Rp {v:,.0f}".replace(",", ".")
    except Exception:
        return "Rp 0"


def parse_int_input(value, extra_value):
    if value == "10+":
        return int(extra_value) if (extra_value is not None and str(extra_value).strip() != "") else 10
    return int(value or 0)


def build_form_context(form_like):
    lb_str = form_like.get("lb", "")
    lt_str = form_like.get("lt", "")

    kt_raw = form_like.get("kt", "")
    km_raw = form_like.get("km", "")
    grs_raw = form_like.get("grs", "")

    kt_more = form_like.get("kt_more", "")
    km_more = form_like.get("km_more", "")
    grs_more = form_like.get("grs_more", "")

    ctx = {
        "lb": lb_str,
        "lt": lt_str,
        "kt": "10+" if kt_raw == "10+" else kt_raw,
        "kt_more": kt_more if kt_raw == "10+" else "",
        "km": "10+" if km_raw == "10+" else km_raw,
        "km_more": km_more if km_raw == "10+" else "",
        "grs": "10+" if grs_raw == "10+" else grs_raw,
        "grs_more": grs_more if grs_raw == "10+" else "",
    }
    return ctx


@app.route("/", methods=["GET"])
def home():
    hasil = session.pop("hasil", None)
    form_data = session.pop("form_data", {})
    resp = make_response(render_template("index.html", hasil=hasil, form=build_form_context(form_data)))
    
    # Tambahkan no-cache header supaya Firefox/Chrome tidak menampilkan popup lama
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp


@app.route("/predict", methods=["POST"])
def predict():
    try:
        lb_str = request.form.get("lb", "")
        lt_str = request.form.get("lt", "")
        kt_raw = request.form.get("kt", "")
        km_raw = request.form.get("km", "")
        grs_raw = request.form.get("grs", "")
        kt_more = request.form.get("kt_more", "")
        km_more = request.form.get("km_more", "")
        grs_more = request.form.get("grs_more", "")

        lb = float(lb_str or 0)
        lt = float(lt_str or 0)
        kt = parse_int_input(kt_raw, kt_more)
        km = parse_int_input(km_raw, km_more)
        grs = parse_int_input(grs_raw, grs_more)

        # Validasi negatif
        for name, val in {"LB": lb, "LT": lt, "KT": kt, "KM": km, "GRS": grs}.items():
            if val < 0:
                flash(f"{name} tidak boleh negatif", "error")
                session["form_data"] = request.form.to_dict()
                return redirect(url_for("home"))

        # Prediksi
        X = pd.DataFrame([[lb, lt, kt, km, grs]], columns=FEATURES)
        y_pred_model = float(model.predict(X)[0])
        y_pred = float(np.expm1(y_pred_model)) if LOG_TARGET else y_pred_model
        hasil = rupiah(y_pred)

        # Simpan hasil & form ke session
        session["hasil"] = hasil
        session["form_data"] = request.form.to_dict()

        return redirect(url_for("home"))

    except Exception as e:
        flash(f"Terjadi error: {e}", "error")
        session["form_data"] = request.form.to_dict()
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

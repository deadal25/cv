import re

# =========================================================
# 🔍 HELPER EXTRACT SECTION
# =========================================================
def extract_section(text, start_keywords, end_keywords):

    text_lower = text.lower()

    start_pos = -1

    # cari keyword awal
    for kw in start_keywords:
        pos = text_lower.find(kw.lower())
        if pos != -1:
            start_pos = pos
            break

    # kalau tidak ditemukan
    if start_pos == -1:
        return ""

    # cari batas akhir terdekat
    end_pos = len(text)

    for end_kw in end_keywords:
        pos = text_lower.find(end_kw.lower(), start_pos + 1)

        if pos != -1 and pos < end_pos:
            end_pos = pos

    return text[start_pos:end_pos].strip()


# =========================================================
# 🎓 PENDIDIKAN
# =========================================================
def extract_education(text):

    return extract_section(
        text,
        [
            "riwayat pendidikan",
            "pendidikan",
            "education"
        ],
        [
            "pengalaman organisasi",
            "pengalaman pekerjaan",
            "pengalaman kerja",
            "work experience",
            "experience",
            "penguasaan bahasa",
            "skill",
            "keahlian",
            "kemampuan",
            "tpa",
            "toefl",
            "ielts",
            "pekerjaan yang disukai"
        ]
    )


# =========================================================
# 💼 PENGALAMAN
# =========================================================
def extract_experience(text):

    pekerjaan = extract_section(
        text,
        [
            "pengalaman pekerjaan",
            "pengalaman kerja",
            "work experience",
            "experience"
        ],
        [
            "pengalaman organisasi",
            "penguasaan bahasa",
            "skill",
            "keahlian",
            "kemampuan",
            "tpa",
            "toefl",
            "ielts",
            "pekerjaan yang disukai"
        ]
    )

    organisasi = extract_section(
        text,
        [
            "pengalaman organisasi",
            "organization experience",
            "organizational experience"
        ],
        [
            "pengalaman pekerjaan",
            "penguasaan bahasa",
            "skill",
            "keahlian",
            "kemampuan",
            "tpa",
            "toefl",
            "ielts",
            "pekerjaan yang disukai"
        ]
    )

    return (pekerjaan + "\n" + organisasi).strip()


# =========================================================
# 🛠️ KEMAMPUAN / SKILL
# =========================================================
def extract_skill(text):

    skill = extract_section(
        text,
        [
            "skill",
            "keahlian",
            "kemampuan",
            "penguasaan bahasa"
        ],
        [
            "pekerjaan yang disukai",
            "hobi",
            "referensi"
        ]
    )

    pekerjaan_disukai = extract_section(
        text,
        [
            "pekerjaan yang disukai"
        ],
        []
    )

    return (skill + "\n" + pekerjaan_disukai).strip()


# =========================================================
# 🧠 PARSE CV STRUCTURED
# =========================================================
def parse_cv_structured(text):

    text_lower = text.lower()

    # =====================================================
    # DEGREE
    # =====================================================
    degree = ""

    if re.search(r"\bs1\b", text_lower):
        degree = "s1"

    elif re.search(r"\bd4\b", text_lower):
        degree = "d4"

    elif re.search(r"\bd3\b", text_lower):
        degree = "d3"

    elif re.search(r"\bsma\b", text_lower):
        degree = "sma"

    elif re.search(r"\bsmk\b", text_lower):
        degree = "smk"

    elif re.search(r"\bsmp\b", text_lower):
        degree = "smp"


    # =====================================================
    # MAJOR
    # =====================================================
    major_keywords = [
        "sistem informasi",
        "informatika",
        "teknik informatika",
        "ilmu komputer",
        "teknik sipil",
        "teknik industri",
        "teknik mesin",
        "teknik elektro",
        "akuntansi",
        "hukum",
        "psikologi",
        "ekonomi",
        "manajemen"
    ]

    major = ""

    for m in major_keywords:
        if m in text_lower:
            major = m
            break


    # =====================================================
    # HASIL PENDIDIKAN
    # =====================================================
    education_section = extract_education(text)

    edu = f"{degree} {major}".strip()

    if education_section:
        edu = education_section


    # =====================================================
    # EXPERIENCE
    # =====================================================
    pengalaman = extract_experience(text)


    # =====================================================
    # SKILL
    # =====================================================
    kemampuan = extract_skill(text)

    # fallback kalau kosong
    if kemampuan.strip() == "":
        kemampuan = text


    # =====================================================
    # RETURN
    # =====================================================
    return {
        "edu": edu,
        "exp": pengalaman,
        "skill": kemampuan,
        "all": text,
        "degree": degree,
        "major": major
    }
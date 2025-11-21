def detect_language_from_filename(filename: str):
    ext = filename.lower().split(".")[-1]
    mapping = {
        "py": "Python",
        "js": "JavaScript",
        "ts": "TypeScript",
        "java": "Java",
        "go": "Go",
        "rb": "Ruby",
        "php": "PHP",
        "cpp": "C++",
        "c": "C",
        "cs": "C#",
        "html": "HTML",
        "css": "CSS",
        "json": "JSON",
        "xml": "XML",
        "rs": "Rust",
        "kt": "Kotlin",
        "swift": "Swift",
        "m": "Objective-C",
        "sh": "Shell",
    }
    return mapping.get(ext, None)

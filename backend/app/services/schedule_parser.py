def parse_schedules(file_content: str):
    parsed_rows = []
    errors = []
    
    lines = file_content.strip().split("\n")
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) == 3:
            date_str, emp_name, shift_name = parts
            parsed_rows.append({
                "date": date_str,
                "employee_name": emp_name,
                "shift_name": shift_name,
                "line": i + 1
            })
        else:
            errors.append(f"Line {i + 1}: Invalid format. Expected DATE | EMPLOYEE_NAME | SHIFT_NAME")
            
    return {
        "parsed_rows": parsed_rows,
        "errors": errors
    }

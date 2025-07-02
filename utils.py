import re
from typing import Optional

def clean_text(text: str) -> str:
    if not text:
        return ""
    
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s\.,/\-:;()%]', ' ', text)
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    return text.strip()

def parse_currency(value: str) -> str:
    if not value:
        return "0,00"
    
    # Remove any non-numeric characters except dots and commas
    cleaned = re.sub(r'[^\d.,]', '', str(value))
    
    # Handle different decimal separators
    if ',' in cleaned and '.' in cleaned:
        # Format: 1.234,56 (Brazilian format)
        if cleaned.rfind(',') > cleaned.rfind('.'):
            cleaned = cleaned.replace('.', '').replace(',', '.')
        # Format: 1,234.56 (US format)
        else:
            cleaned = cleaned.replace(',', '')
    elif ',' in cleaned:
        # Check if it's a decimal separator or thousands separator
        comma_pos = cleaned.rfind(',')
        after_comma = cleaned[comma_pos + 1:]
        
        # If 2 digits after comma, it's probably decimal
        if len(after_comma) == 2:
            cleaned = cleaned.replace(',', '.')
        # Otherwise, it's thousands separator
        else:
            cleaned = cleaned.replace(',', '')
    
    try:
        # Convert to float and back to ensure valid number
        float_value = float(cleaned)
        
        # Format as Brazilian currency
        return f"{float_value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        return "0,00"

def parse_date(date_str: str) -> str:
    """
    Normaliza formato de data.
    
    Args:
        date_str (str): Data em formato string
        
    Returns:
        str: Data no formato DD/MM/AAAA
    """
    if not date_str:
        return ""
    
    # Remove any non-numeric characters except slashes and dashes
    cleaned = re.sub(r'[^\d/\-]', '', str(date_str))
    
    # Replace dashes with slashes
    cleaned = cleaned.replace('-', '/')
    
    # Validate date format
    date_pattern = r'^\d{2}/\d{2}/\d{4}$'
    if re.match(date_pattern, cleaned):
        return cleaned
    
    # Try to extract date parts
    parts = re.findall(r'\d+', cleaned)
    if len(parts) >= 3:
        day, month, year = parts[0], parts[1], parts[2]
        
        # Ensure proper formatting
        day = day.zfill(2)
        month = month.zfill(2)
        
        # Handle 2-digit years
        if len(year) == 2:
            current_year = 2025  # Based on the current date provided
            if int(year) <= 30:
                year = f"20{year}"
            else:
                year = f"19{year}"
        
        return f"{day}/{month}/{year}"
    
    return date_str

def extract_numeric_value(text: str) -> Optional[float]:
    """
    Extrai valor numérico de uma string.
    
    Args:
        text (str): Texto contendo valor numérico
        
    Returns:
        Optional[float]: Valor numérico extraído ou None
    """
    if not text:
        return None
    
    # Find all numeric patterns
    patterns = [
        r'(\d+[.,]\d{2})',  # Decimal with 2 places
        r'(\d+[.,]\d+)',    # Any decimal
        r'(\d+)'            # Integer only
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, str(text))
        if matches:
            try:
                # Use the last match (usually the most relevant)
                value_str = matches[-1].replace(',', '.')
                return float(value_str)
            except (ValueError, TypeError):
                continue
    
    return None

def validate_cnpj(cnpj: str) -> bool:
    """
    Valida formato de CNPJ.
    
    Args:
        cnpj (str): CNPJ para validar
        
    Returns:
        bool: True se o formato estiver correto
    """
    if not cnpj:
        return False
    
    # Check CNPJ format: XX.XXX.XXX/XXXX-XX
    pattern = r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$'
    return bool(re.match(pattern, cnpj))

def validate_access_key(key: str) -> bool:
    """
    Valida chave de acesso da NF-e.
    
    Args:
        key (str): Chave de acesso para validar
        
    Returns:
        bool: True se o formato estiver correto
    """
    if not key:
        return False
    
    # Remove spaces and check if it's 44 digits
    clean_key = re.sub(r'\s', '', key)
    return len(clean_key) == 44 and clean_key.isdigit()

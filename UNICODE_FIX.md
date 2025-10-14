# Unicode Encoding Fix for Windows

## Problem
When running MaiOpinion on Windows, the follow-up agent was throwing this error:
```
'charmap' codec can't encode character '\u2705' in position 18: character maps to <undefined>
```

## Root Cause
- Windows PowerShell uses 'cp1252' (charmap) encoding by default
- Python's print() function uses the console's default encoding
- Unicode characters like emojis (✅, 📧) cannot be encoded in cp1252
- The error occurred when printing messages with emojis to the console

## Solution Applied

### 1. Removed Emojis from Print Statements
Changed:
- `✅ Patient registered` → `[OK] Patient registered`
- `📧 FOLLOW-UP EMAIL` → `[FOLLOW-UP EMAIL]`

### 2. Added Safe Print Function
Created a helper function to handle Unicode encoding errors:

```python
def safe_print(message: str):
    """Safely print message, handling Unicode encoding issues on Windows"""
    try:
        print(message)
    except UnicodeEncodeError:
        # Fallback to ASCII if console can't handle Unicode
        print(message.encode('ascii', errors='replace').decode('ascii'))
```

### 3. Updated Email Content Printing
Changed line 364 in `agents/followup.py`:
```python
# Before
print(email_content)

# After
safe_print(email_content)
```

## Files Modified
- `agents/followup.py`:
  - Added `safe_print()` function
  - Removed emoji from line 182
  - Removed emoji from line 331 (email header)
  - Changed `print()` to `safe_print()` for email content

## CSV File Handling
Note: CSV file operations already had `encoding='utf-8'` specified, so they were not the source of the error:
```python
with open(self.db_path, 'w', newline='', encoding='utf-8') as f:
```

## Testing
To verify the fix works:
```powershell
python main.py -i .\sample_data\sample_lungs.png -c "Test condition" -e test@example.com
```

Should now complete without Unicode errors.

## Alternative Solutions (Not Used)

### Option 1: Change Console Encoding
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```
- Pros: Allows full Unicode support
- Cons: Requires user to run this before every session

### Option 2: Set Python Environment Variable
```powershell
$env:PYTHONIOENCODING = "utf-8"
```
- Pros: Affects all Python print statements
- Cons: May cause issues with other tools

### Option 3: Use sys.stdout.reconfigure()
```python
import sys
sys.stdout.reconfigure(encoding='utf-8')
```
- Pros: Programmatic solution
- Cons: May not work on all Windows versions

## Why Our Solution is Best
- ✅ No user configuration required
- ✅ Backward compatible
- ✅ Works on all Windows versions
- ✅ Graceful degradation (replaces unsupported chars with '?')
- ✅ Maintains readability

## Future Considerations
If you want to keep emojis for better UX:
1. Use `safe_print()` for all print statements
2. Or detect Windows and conditionally use emojis:
   ```python
   import platform
   is_windows = platform.system() == 'Windows'
   check_mark = '[OK]' if is_windows else '✅'
   ```

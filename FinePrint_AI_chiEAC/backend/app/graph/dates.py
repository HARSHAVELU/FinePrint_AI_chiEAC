"""Date arithmetic requires an explicit unambiguous anchor, never upload time."""
import re
from datetime import date,timedelta
from ..schemas import Item

def relative_deadlines(rows):
    items=[]
    for row in rows:
        # Narrow deterministic syntax deliberately avoids choosing among anchors.
        match=re.search(r'within (\d{1,3}) (business |calendar )?days (?:after|of) (\d{4}-\d{2}-\d{2})',row.text,re.I)
        if not match:continue
        days=int(match[1]);anchor=date.fromisoformat(match[3]);business=(match[2] or '').strip().lower()=='business'
        if business:
            # Holidays are not inferred. Keep unresolved until a calendar is supplied.
            value='Not resolved: '+match[0]
            arithmetic='Business-day calendar and holidays are not stated; confirm the exact date with the sender.'
        else:
            value=(anchor+timedelta(days=days)).isoformat();arithmetic=f'{anchor.isoformat()} + {days} calendar days = {value}.'
        items.append(Item(item_type='deadline',value=value,section_id=row.section_id,quote=match[0],confidence=.75,inference=arithmetic))
    return items

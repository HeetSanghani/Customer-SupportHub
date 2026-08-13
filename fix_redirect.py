import os
import re

files = [
    "supporthub/frontend/src/components/EmailInbox.jsx",
    "supporthub/frontend/src/components/InstagramInbox.jsx",
    "supporthub/frontend/src/components/WhatsAppInbox.jsx"
]

for fpath in files:
    with open(fpath, "r") as f:
        content = f.read()

    # 1. Remove isResolvingRef and add lockedTicketId
    content = re.sub(r'const isResolvingRef = useRef\(false\)', r'const [lockedTicketId, setLockedTicketId] = useState(null)', content)

    # 2. Update useEffect
    use_effect_old = r'useEffect\(\(\) => \{\n\s*if \(isResolvingRef\.current\) return;'
    use_effect_new = r'''useEffect(() => {
    if (lockedTicketId) {
      if (selectedTicketId !== lockedTicketId) {
        setSelectedTicketId(lockedTicketId)
      }
      return;
    }'''
    content = re.sub(use_effect_old, use_effect_new, content)

    # 3. Update onMutate (remove isResolvingRef, add setLockedTicketId)
    on_mutate_old = r'onMutate: async \(newData\) => \{\n\s*isResolvingRef\.current = true;'
    on_mutate_new = r'onMutate: async (newData) => {\n      setLockedTicketId(selectedTicketId);'
    content = re.sub(on_mutate_old, on_mutate_new, content)

    # 4. Update onError (remove isResolvingRef)
    on_error_old = r'queryClient\.setQueryData\(\[(.*?)\]\, context\.previousTickets\)\n\s*isResolvingRef\.current = false;'
    on_error_new = r'queryClient.setQueryData([\1], context.previousTickets)'
    content = re.sub(on_error_old, on_error_new, content)

    # 5. Update onSettled (remove setTimeout)
    on_settled_old = r'queryClient\.invalidateQueries\(\{ queryKey: \[(.*?)\] \}\)\.then\(\(\) => \{\n\s*setTimeout\(\(\) => \{ isResolvingRef\.current = false \}, 2000\);\n\s*\}\)'
    on_settled_new = r'queryClient.invalidateQueries({ queryKey: [\1] })'
    content = re.sub(on_settled_old, on_settled_new, content)

    # 6. Update tab click
    tab_click_old = r'onClick\{\(\) => setStatusFilter\(tab\.id\)\}'
    tab_click_new = r'onClick={() => { setStatusFilter(tab.id); setLockedTicketId(null); }}'
    content = re.sub(tab_click_old, tab_click_new, content)
    
    # Wait, the exact string in the files is: onClick={() => setStatusFilter(tab.id)}
    content = content.replace("onClick={() => setStatusFilter(tab.id)}", "onClick={() => { setStatusFilter(tab.id); setLockedTicketId(null); }}")

    # 7. Update ticket click
    ticket_click_old = r'onClick\{\(\) => setSelectedTicketId\(ticket\.id\)\}'
    ticket_click_new = r'onClick={() => { setSelectedTicketId(ticket.id); setLockedTicketId(null); }}'
    # The exact string is: onClick={() => setSelectedTicketId(ticket.id)}
    content = content.replace("onClick={() => setSelectedTicketId(ticket.id)}", "onClick={() => { setSelectedTicketId(ticket.id); setLockedTicketId(null); }}")

    with open(fpath, "w") as f:
        f.write(content)
        
print("Updated successfully")

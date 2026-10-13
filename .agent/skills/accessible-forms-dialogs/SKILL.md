---
name: accessible-forms-dialogs
description: >-
  Provides guidelines and validation checklists for accessible WAI-ARIA forms, modal dialogs, and interactive controls in React and Next.js applications. Use this skill when implementing, styling, or auditing forms, inputs, select dropdowns, modals, focus trapping, keyboard navigation, or resolving Chrome DevTools accessibility audits.
---

# Accessible Forms, Modals & Dialogs (WAI-ARIA Guide)

This skill ensures that all user input elements, modals, and interaction states are accessible, screen-reader compliant, and pass Chrome DevTools accessibility audits.

---

## 1. Strict Label Association Rule

Every `<input>`, `<select>`, and `<textarea>` must have an explicit label association.

### Correct Pattern
```tsx
<div>
  <label htmlFor="user-txn-amount" className="block text-xs font-bold text-slate-700 mb-1">
    Amount (৳) <span className="text-rose-500">*</span>
  </label>
  <input
    id="user-txn-amount"
    name="amount"
    type="number"
    step="0.01"
    required
    aria-required="true"
    placeholder="1,500.00"
    value={amount}
    onChange={(e) => setAmount(e.target.value)}
    className="w-full rounded-xl border border-slate-300 px-3.5 py-2.5 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-navy-900"
  />
</div>
```

### Prohibited Patterns
- Never wrap inputs inside `<label>` without an explicit `htmlFor` and `id`.
- Never use placeholder text as a replacement for a visible label.
- Never omit `aria-label` or `aria-labelledby` on icon-only buttons (e.g. `<button aria-label="Close modal"><X className="h-4 w-4" /></button>`).

---

## 2. Modal Dialog Accessibility Checklist

When implementing modals or overlays:
1. **Modal Attributes**:
   - `role="dialog"`
   - `aria-modal="true"`
   - `aria-labelledby="modal-title-id"`
2. **Keyboard Trapping**:
   - Pressing `Escape` must close the dialog.
   - Initial focus must be directed to the first interactive element or the close button.
   - Focus must not escape into background page elements while open.
3. **Backdrop Blur**:
   - Overlay must use `bg-slate-900/60 backdrop-blur-sm`.
   - Clicking the backdrop outside the modal card should trigger `onClose()`.

### Accessible Modal Skeleton
```tsx
export function AccessibleModal({ isOpen, onClose, title, children }: Props) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    if (isOpen) window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm"
      role="dialog"
      aria-modal="true"
      aria-labelledby="dialog-title"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl border border-slate-100">
        <div className="flex items-center justify-between pb-3 border-b">
          <h2 id="dialog-title" className="text-base font-black text-navy-900">
            {title}
          </h2>
          <button
            onClick={onClose}
            className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-600"
            aria-label="Close dialog"
          >
            <X className="h-4 w-4" aria-hidden="true" />
          </button>
        </div>
        <div className="mt-4">{children}</div>
      </div>
    </div>
  );
}
```

---

## 3. Chrome DevTools Audit Verification Runbook
1. Open page in Chrome via MCP (`navigate_page`).
2. Run `list_console_messages` to check for:
   - `No label associated with a form field`
   - `Incorrect use of <label for=FORM_ELEMENT>`
3. If issues are found, inspect the DOM tree and ensure matching `htmlFor` and `id` pairs.

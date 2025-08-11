## **Overview**

This is a **full-screen, minimalistic, neon-themed calculator** built with **Python Tkinter**.
It combines:

* A **modern circular button UI** (black background, green glow).
* **History tracking** of all previous calculations.
* **Full unit conversion** (Length, Weight, Temperature, Time, Data) — results are stored in history for reuse.

---

## **Main Features**

### **1. Modern Calculator**

* Circular green buttons with hover effect.
* Large display using a modern monospace font.
* Multiplication shown as **×** but works as `*`.
* Supports advanced math:

  * Square root (√)
  * Exponentiation (^)
  * Modulus (%)
  * Brackets `( )` for grouped expressions.

### **2. History Panel**

* Stores all calculations and conversions.
* Double-click an entry to reuse it in a new calculation.

### **3. Unit Converter**

* Located under the history panel.
* Categories:

  * **Length**: m, km, cm, mile, yard, foot, inch
  * **Weight**: kg, g, lb, oz
  * **Temperature**: °C, °F, K
  * **Time**: sec, min, hr, day
  * **Data**: bit, byte, KB, MB, GB
* Conversion results automatically appear in the history for easy reuse.

---

## **How It Works**

* **UI**: Built with `tkinter` and a custom `CircularButton` class for perfect round buttons.
* **Calculator Logic**:

  * Stores input as a string `expression`.
  * Buttons append characters to `expression`.
  * On `=`, evaluates with Python’s `eval()` (safe for internal use).
* **History**: Maintained in a list and a `Listbox`.
* **Unit Conversion**:

  * Uses predefined conversion factors for each category.
  * Temperature uses formulas for °C, °F, K.
  * Results are added to history and can be reused.

---

* **One app** for both calculations & conversions.
* **Fast reuse** of past results via history.
* **Aesthetic**: dark theme, neon green UI, large readable display.
* **Simple deploy**: just Python + Tkinter (no extra dependencies).

---

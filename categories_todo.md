# Plan: Update Category Pie Chart & List UI

## 1. Category List Panel (Left Side)
- Display all categories with:
  - Emoji icon for each category (choose emoji based on category name).
  - Category name.
  - Total amount (formatted as "$xx.xxx").
- Sort categories by amount descending.
- Responsive: Stack above pie chart on mobile.

## 2. Pie Chart (Right Side)
- Donut chart (with inner radius).
- No percentage in legend or on chart.
- Legend outside the chart, showing only category name and color.
- Tooltip on hover shows only the amount (formatted as "$xx.xxx").
- No labels on the chart slices.

## 3. Layout
- Desktop: Flex row, category list left, pie chart right.
- Mobile: Stack vertically (category list above pie chart).

## 4. Styling
- Clean, modern look.
- Use emoji for icons.
- Consistent spacing, fonts, and colors.
- Hover effect on pie slices and list items.

## 5. Data
- Category names and amounts come from backend.
- Format all amounts as "$xx.xxx" (thousands separator).

## 6. Implementation Steps
1. Create/Update CategoryList component to show emoji, name, and amount.
2. Refactor CategoryPieChart:
   - Remove percentage from legend and chart.
   - Show only color and name in legend.
   - Tooltip shows only amount.
   - Make chart a donut.
3. Update layout for responsiveness.
4. Style components to match the reference.
5. Test on desktop and mobile.

---
**Questions answered:**
1. Use emojis for icons.
2. Sort by amount descending.
3. Category names from backend.
4. Amounts formatted as "$xx.xxx".
5. Stack vertically on mobile.
6. Legend
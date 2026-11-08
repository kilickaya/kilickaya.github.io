(() => {
  const root = document.documentElement;
  const toggle = document.querySelector(".theme-toggle");
  // Start new visits in light mode; retain an explicit choice within this tab.
  const key = "session-theme";
  const setTheme = (theme) => {
    const dark = theme === "dark";
    root.dataset.theme = dark ? "dark" : "light";
    toggle.textContent = dark ? "Light" : "Dark";
    toggle.setAttribute(
      "aria-label",
      `Switch to ${dark ? "light" : "dark"} theme`,
    );
    toggle.setAttribute("aria-pressed", String(dark));
  };
  try {
    setTheme(sessionStorage.getItem(key));
  } catch {
    setTheme("light");
  }
  toggle.hidden = false;
  toggle.addEventListener("click", () => {
    const theme = root.dataset.theme === "dark" ? "light" : "dark";
    setTheme(theme);
    try {
      sessionStorage.setItem(key, theme);
    } catch {
      /* Theme still works without storage. */
    }
  });
  // Mark the section being read without changing scroll position or URL history.
  const sectionLinks = [
    ...document.querySelectorAll('.site-header nav a[href^="#"]'),
  ];
  if ("IntersectionObserver" in window && sectionLinks.length) {
    const sections = sectionLinks.map((link) =>
      document.getElementById(link.hash.slice(1)),
    );
    const visible = new Set();
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) visible.add(entry.target);
          else visible.delete(entry.target);
        });
        const current = sections
          .filter((section) => visible.has(section))
          .at(-1);
        sectionLinks.forEach((link, i) => {
          if (sections[i] === current)
            link.setAttribute("aria-current", "location");
          else link.removeAttribute("aria-current");
        });
      },
      { rootMargin: "-112px 0px -60% 0px", threshold: 0 },
    );
    sections.filter(Boolean).forEach((section) => observer.observe(section));
  }
})();

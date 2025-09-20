<p align="center">
  <h2 align="center">XianMalik CV</h2>
</p>

<p align="center">
    Professional LaTeX CV Template powered by XeLaTeX & Inter Font Family
</p>

<p align="center">
    <!-- <a href="https://github.com/xianmalik/xianmalik_resume/issues">
        <img alt="Issues" src="https://img.shields.io/github/issues/xianmalik/xianmalik_resume?style=for-the-badge&logo=bilibili&color=F5E0DC&logoColor=D9E0EE&labelColor=302D41"></a> -->
    <a href="https://github.com/xianmalik/xianmalik_resume">
        <img alt="Repo Size" src="https://img.shields.io/github/repo-size/xianmalik/xianmalik_resume?color=%23DDB6F2&label=SIZE&logo=square&style=for-the-badge&logoColor=D9E0EE&labelColor=302D41"/></a>
    <a href="https://github.com/xianmalik/xianmalik_resume/stargazers">
        <img alt="Stars" src="https://img.shields.io/github/stars/xianmalik/xianmalik_resume?style=for-the-badge&logo=starship&color=C9CBFF&logoColor=D9E0EE&labelColor=302D41"></a>
</p>

<hr />

<p align="center">
    <h2 align="center">Tech Stack</h2>
</p>

<p align="center">
    <a href="https://www.latex-project.org/"><img src="https://img.shields.io/badge/LaTeX-302D41?style=for-the-badge&logo=latex&logoColor=008080" /></a>
    <a href="https://tug.org/xetex/"><img src="https://img.shields.io/badge/XeLaTeX-302D41.svg?logo=latex&logoColor=white&style=for-the-badge" /></a>
    <a href="https://rsms.me/inter/"><img src="https://img.shields.io/badge/Inter_Font-302D41?logo=googlefonts&logoColor=4285F4&style=for-the-badge" /></a>
    <a href="https://fontawesome.com/"><img src="https://img.shields.io/badge/Font_Awesome-302D41?logo=fontawesome&logoColor=528DD7&style=for-the-badge"/></a>
</p>

<hr />

<p align="center">
    <h2 align="center">Quick Start</h2>
</p>

```bash
# Build the CV
./scripts/build.sh

# Watch for changes (if available)
./scripts/watch.sh

# Clean output files
./scripts/clean.sh
```

<p align="center">
    <h2 align="center">Project Structure</h2>
</p>

```
├── cv/                     # CV content sections
│   ├── 00-summary.tex
│   ├── 01-experience.tex
│   ├── 02-education.tex
│   ├── 03-projects.tex
│   ├── 04-skills.tex
│   └── 05-languages.tex
├── font/                   # Inter font family
├── output/                 # Generated PDF output
├── scripts/                # Build automation scripts
├── resume.tex             # Main LaTeX file
└── xianmalik.cls          # Custom CV class
```

<p align="center">
    <h2 align="center">Features</h2>
</p>

- **Modern Design** - Clean and professional layout
- **Customizable** - Easy to modify colors, fonts, and structure
- **Responsive** - Optimized for both screen and print
- **Fast Build** - Efficient compilation with colorized output
- **Auto Cleanup** - Automatic removal of auxiliary files
- **Minimalist** - Only essential code, no bloat

<p align="center">
    <h2 align="center">Requirements</h2>
</p>

- XeLaTeX (TeX Live or MiKTeX)
- Inter font family (included in `/font` directory)
- Font Awesome 5 package

<p align="center">
    <h2 align="center">Usage</h2>
</p>

1. **Clone the repository**
   ```bash
   git clone https://github.com/xianmalik/xianmalik_cv.git
   cd xianmalik_cv
   ```

2. **Customize your information**
   - Edit `resume.tex` for personal details
   - Modify files in `/cv` directory for content

3. **Build your CV**
   ```bash
   ./scripts/build.sh
   ```

4. **Find your PDF**
   - Generated CV will be in `/output/resume.pdf`

<p align="center">
    <h2 align="center">Customization</h2>
</p>

- **Colors**: Modify accent color in `xianmalik.cls`
- **Fonts**: Update font specifications in the class file
- **Layout**: Adjust spacing and margins in the configuration section
- **Content**: Edit individual section files in the `/cv` directory

<p align="center">
    <h2 align="center">License</h2>
</p>

<p align="center">
This project is open source and available under the <a href="LICENSE">MIT License</a>.
</p>

<p align="center">
    <h2 align="center">Author</h2>
</p>

<p align="center">
    <strong>Malik Zubayer Ul Haider</strong><br>
    <a href="https://xianmalik.com">Website</a> •
    <a href="https://github.com/xianmalik">GitHub</a> •
    <a href="https://linkedin.com/in/xianmalik">LinkedIn</a>
</p>
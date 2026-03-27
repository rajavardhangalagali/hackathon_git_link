# 📹 How to Add Demo Video/Screenshots

## Option 1: Add Video File (Recommended)

### Step 1: Record Your Demo
- Use OBS Studio, ShareX, or Windows Game Bar
- Record your app in action (2-3 minutes)
- Save as MP4 format
- Keep file size under 10MB for GitHub

### Step 2: Add to Repository

**Method A: Direct Upload (Easiest)**
1. Go to your GitHub repository
2. Click "Edit" on README.md
3. Drag and drop your `demo.mp4` file into the editor
4. GitHub will automatically upload and generate a link
5. Copy the generated link
6. Replace the demo section in README

**Method B: Add to Repo**
```bash
# Add video to root folder
cp /path/to/your/demo.mp4 wifi-security-auditor/demo.mp4

# Or add to assets folder
mkdir -p wifi-security-auditor/assets
cp /path/to/your/demo.mp4 wifi-security-auditor/assets/demo.mp4
```

Then update README:
```markdown
![Demo](./demo.mp4)
# or
![Demo](./assets/demo.mp4)
```

### Step 3: Update .gitignore (if video is large)

If your video is over 10MB, add to `.gitignore`:
```bash
# Large media files
*.mp4
*.mov
*.avi
```

Then use Git LFS or host elsewhere.

---

## Option 2: Convert to GIF

### Why GIF?
- ✅ Smaller file size
- ✅ Auto-plays on GitHub
- ✅ No external hosting needed
- ✅ Works everywhere

### How to Convert:

**Using Online Tool:**
1. Go to https://ezgif.com/video-to-gif
2. Upload your MP4
3. Set size to 800px width
4. Convert and download

**Using FFmpeg:**
```bash
# Install ffmpeg first
# Windows: choco install ffmpeg
# Mac: brew install ffmpeg
# Linux: sudo apt install ffmpeg

# Convert video to GIF
ffmpeg -i demo.mp4 -vf "fps=10,scale=800:-1:flags=lanczos" -c:v gif demo.gif
```

### Add GIF to Repo:
```bash
cp demo.gif wifi-security-auditor/demo.gif
```

Update README:
```markdown
![Demo](./demo.gif)
```

---

## Option 3: Add Screenshots

### Step 1: Take Screenshots

**Windows:**
- Press `Win + Shift + S` for Snipping Tool
- Or use `Win + PrtScn` for full screen

**Mac:**
- Press `Cmd + Shift + 4` for selection
- Or `Cmd + Shift + 3` for full screen

**Linux:**
- Use `gnome-screenshot` or `flameshot`

### Step 2: Organize Screenshots

```bash
# Create screenshots folder
mkdir wifi-security-auditor/screenshots

# Add your screenshots
cp dashboard.png wifi-security-auditor/screenshots/
cp network-map.png wifi-security-auditor/screenshots/
cp analytics.png wifi-security-auditor/screenshots/
cp alerts.png wifi-security-auditor/screenshots/
cp settings.png wifi-security-auditor/screenshots/
```

### Step 3: Update README

Screenshots are already configured in README:
```markdown
![Dashboard](./screenshots/dashboard.png)
![Network Map](./screenshots/network-map.png)
![Analytics](./screenshots/analytics.png)
```

---

## 📏 Recommended Sizes

### Video:
- **Resolution:** 1920x1080 or 1280x720
- **Duration:** 2-3 minutes
- **File Size:** Under 10MB
- **Format:** MP4 (H.264)
- **FPS:** 30fps

### GIF:
- **Width:** 800px (height auto)
- **File Size:** Under 5MB
- **FPS:** 10-15fps
- **Colors:** 256 colors

### Screenshots:
- **Resolution:** 1920x1080 (full HD)
- **Format:** PNG (for quality) or JPG (for size)
- **File Size:** Under 500KB each

---

## 🎬 What to Show in Demo

### Essential Scenes (30 seconds each):

1. **Welcome Screen**
   - Show the landing page
   - Click "Start Scanning"

2. **Dashboard Loading**
   - Show scanning in progress
   - Networks appearing

3. **Network Map**
   - Interactive visualization
   - Drag nodes around
   - Show connected network

4. **Analytics Charts**
   - Encryption distribution
   - Signal strength
   - Risk heatmap

5. **Alerts Panel**
   - Show live alerts
   - Different severity levels

6. **Settings**
   - Open settings modal
   - Show Telegram configuration

7. **PDF Report**
   - Click "Generate Report"
   - Show downloaded PDF

---

## 📤 Pushing to GitHub

### If Using Video/GIF:

```bash
# Add files
git add demo.gif screenshots/

# Commit
git commit -m "Add demo video and screenshots"

# Push
git push origin main
```

### If Video is Too Large:

**Option A: Use Git LFS**
```bash
# Install Git LFS
git lfs install

# Track video files
git lfs track "*.mp4"
git lfs track "*.gif"

# Add and commit
git add .gitattributes demo.mp4
git commit -m "Add demo video with Git LFS"
git push origin main
```

**Option B: Host Externally**
- Upload to Google Drive
- Upload to Imgur (for GIFs)
- Use GitHub Releases
- Link in README

---

## ✅ Final Checklist

Before pushing:
- [ ] Video/GIF is under 10MB
- [ ] Screenshots are clear and high quality
- [ ] All images are in correct folders
- [ ] README links are updated
- [ ] .gitignore is configured (if needed)
- [ ] Tested locally that images display
- [ ] Ready to push to GitHub

---

## 🎯 Quick Commands

```bash
# Create folders
mkdir -p screenshots assets

# Add demo files
cp /path/to/demo.gif ./demo.gif
cp /path/to/screenshots/*.png ./screenshots/

# Check file sizes
ls -lh demo.gif screenshots/

# Add to git
git add demo.gif screenshots/ README.md
git commit -m "Add demo and screenshots"
git push origin main
```

---

## 💡 Pro Tips

1. **Compress images** before adding:
   - Use TinyPNG.com for PNG files
   - Use JPEGmini.com for JPG files

2. **Optimize GIF**:
   - Use ezgif.com optimizer
   - Reduce colors to 128 or 64
   - Lower FPS to 10

3. **Test locally first**:
   - View README in VS Code preview
   - Check all images load

4. **Use relative paths**:
   - `./demo.gif` not `/demo.gif`
   - Works on GitHub and locally

5. **Add alt text**:
   - `![Dashboard Screenshot](./screenshots/dashboard.png)`
   - Helps with accessibility

---

Your demo is ready to be added! 🎉

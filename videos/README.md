# Teaching Videos Directory

This directory contains promotional teaching videos for the ChinaBridge Academy dashboard.

## How to Upload Videos

### Video File Naming
Upload your videos with these names:
1. **csca_math_lesson.mp4** - CSCA Math Lesson by Phoenix
2. **ielts_speaking.mp4** - IELTS Speaking Practice by Serum
3. **chinese_fundamentals.mp4** - Chinese Language Fundamentals by Phoenix

### Video Requirements
- **Format**: MP4 (H.264 video, AAC audio)
- **Recommended Resolution**: 1280x720 (720p) or higher
- **Bitrate**: 1000-2000 kbps for good quality/file size balance
- **Max Duration**: 10-15 minutes per video (for promotional purposes)

### Security Features
- Videos are served through the `/api/video/<id>` endpoint
- Users **cannot download** videos:
  - Right-click download is disabled
  - Context menu is disabled on the player
  - Download button is hidden via `controlsList="nodownload"`
- Only authenticated users can see the videos

### Upload Instructions

1. **Prepare your video** in MP4 format
2. **Place the file** in this directory (`videos/`)
3. **Name it** according to the mapping above
4. **Test** by logging into the dashboard - videos will appear immediately

### Converting Videos to MP4

**Using FFmpeg** (recommended):
```bash
# Convert any video to MP4
ffmpeg -i input_video.mov -vcodec h264 -acodec aac output.mp4

# Optimize for web (reduce file size)
ffmpeg -i input.mp4 -vf scale=1280:720 -b:v 1500k -maxrate 1500k -bufsize 3000k output.mp4
```

### File Size Estimate
- 10-minute video at 1500 kbps ≈ 110-130 MB
- Consider compression if file size is too large

### Troubleshooting

**Video not showing in dashboard?**
1. Check filename matches exactly (case-sensitive on some servers)
2. Verify file is valid MP4 format
3. Check server logs for errors

**Video plays but won't stream?**
1. Ensure server can read the file
2. Check file permissions (should be readable by web server)
3. Verify path in `server.py` VIDEO_MAPPING is correct

### Adding More Videos

To add more videos:
1. Add video ID and filename to `VIDEO_MAPPING` in `server.py`
2. Add video object to `teachingVideos` array in `dashboard.html`
3. Place video file in this directory
4. Restart server

Example:
```python
# In server.py
VIDEO_MAPPING = {
    1: 'csca_math_lesson.mp4',
    2: 'ielts_speaking.mp4',
    3: 'chinese_fundamentals.mp4',
    4: 'new_video.mp4'  # Add new video
}
```

```javascript
// In dashboard.html
const teachingVideos = [
    { id: 1, title: 'CSCA Math Lesson', tutor: 'Phoenix', description: '...' },
    { id: 2, title: 'IELTS Speaking Practice', tutor: 'Serum', description: '...' },
    { id: 3, title: 'Chinese Language Fundamentals', tutor: 'Phoenix', description: '...' },
    { id: 4, title: 'New Lesson Title', tutor: 'Tutor Name', description: '...' }  // Add here
];
```

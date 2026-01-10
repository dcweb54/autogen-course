# 🎯 Complete Manual: How to Fully Utilize the Modular Poster Generator

This manual will walk you through **everything** you need to know to create stunning posters with zero guesswork.

---

## 📁 Step 1: Setup Your Project Structure

Create this exact folder structure:

```
my-poster-project/
├── main.py                 # Your main script
├── poster_template.json    # Your design template
├── fonts/                  # Your font files
│   ├── arial.ttf
│   └── montserrat-bold.ttf
├── backgrounds/            # Your background images
│   └── nature.jpg
└── output/                 # Generated posters go here
```

---

## 🎨 Step 2: Create Your Design Template

Create `poster_template.json` with this structure:

```json
{
  "canvas": {
    "width": 1080,
    "height": 1350,
    "background_color": "#000000"
  },
  "image_area": {
    "height_percent": 0.65
  },
  "bottom_overlay": {
    "height_percent": 0.35,
    "gradient": {
      "from_rgba": [0, 0, 0, 230],
      "to_rgba": [0, 0, 0, 0]
    }
  },
  "slide_indicator": {
    "enabled": true,
    "margin": [28, 28],
    "box": {
      "width": 110,
      "height": 60,
      "bg_color": [0, 0, 0, 180],
      "corner_radius": 30
    },
    "text_style": {
      "font_path": "fonts/arial.ttf",
      "font_size": 28,
      "color": "#FFFFFF"
    }
  },
  "myth_label": {
    "text": "#Myth 3",
    "position": {
      "y_offset_percent_from_overlay_top": 0.06
    },
    "style": {
      "font_path": "fonts/arial.ttf",
      "font_size": 54,
      "color": "#FF8A50"
    }
  },
  "myth_statement": {
    "text": "✖ Detox Diets Cleanse the Body",
    "position": {
      "y_offset_percent_from_overlay_top": 0.18
    },
    "style": {
      "font_path": "fonts/arial.ttf",
      "font_size": 44,
      "color": "#FF8A50"
    },
    "icon": {
      "draw_x_icon": true,
      "x_icon": {
        "circle_radius": 26,
        "circle_color": "#FF3B30",
        "x_color": "#FFFFFF",
        "x_thickness": 6,
        "pad_right": 10
      }
    }
  },
  "truth_label": {
    "text": "Truth:",
    "position": {
      "y_offset_percent_from_overlay_top": 0.28
    },
    "style": {
      "font_path": "fonts/arial.ttf",
      "font_size": 40,
      "color": "#B9FF7A",
      "underline": true
    }
  },
  "truth_explanation": {
    "text": "Your liver & kidneys are natural detox systems. Juices just give sugar and may cause nutrient imbalance.",
    "position": {
      "y_offset_percent_from_overlay_top": 0.38
    },
    "style": {
      "font_path": "fonts/arial.ttf",
      "font_size": 30,
      "color": "#FFFFFF",
      "max_width_percent": 0.9,
      "line_spacing": 8
    }
  },
  "margins": {
    "left_percent": 0.05,
    "right_percent": 0.05
  }
}
```

---

## 🚀 Step 3: Create Your Main Script

Create `main.py`:

```python
from PIL import Image
import sys
import os

# Add the modular poster generator code here
# (Copy the complete code from the previous response)

def create_health_myth_poster():
    """Example: Create a health myth poster"""
    bg_path = "backgrounds/nature.jpg"
    out_path = "output/health-myth-01.jpg"
    template_path = "poster_template.json"
    
    gen_poster(bg_path, out_path, template_path)

def create_custom_poster(myth_text: str, truth_text: str, bg_image: str, output_name: str):
    """Create a custom poster with your own content"""
    # Load and modify template
    template = load_template("poster_template.json")
    
    # Update the text content
    template["myth_statement"]["text"] = f"✖ {myth_text}"
    template["truth_explanation"]["text"] = truth_text
    
    # Save modified template temporarily
    temp_template = f"temp_{output_name}.json"
    with open(temp_template, "w") as f:
        json.dump(template, f, indent=2)
    
    # Generate poster
    gen_poster(bg_image, f"output/{output_name}.jpg", temp_template)
    
    # Clean up temp file
    os.remove(temp_template)

if __name__ == "__main__":
    # Method 1: Use existing template as-is
    create_health_myth_poster()
    
    # Method 2: Create custom content
    create_custom_poster(
        myth_text="You Need 8 Glasses of Water Daily",
        truth_text="Water needs vary by person, activity, and climate. Listen to your body's thirst signals!",
        bg_image="backgrounds/water.jpg",
        output_name="water-myth"
    )
    
    print("✅ All posters generated successfully!")
```

---

## 🛠️ Step 4: Advanced Customization Guide

### 🎯 **Positioning Cheat Sheet**
Use these `y_offset_percent_from_overlay_top` values as starting points:

| Component | Conservative | Balanced | Spacious |
|-----------|--------------|----------|----------|
| Myth Label | 0.04 | 0.06 | 0.08 |
| Myth Statement | 0.14 | 0.18 | 0.22 |
| Truth Label | 0.24 | 0.28 | 0.32 |
| Truth Explanation | 0.32 | 0.38 | 0.44 |

### 🎨 **Color Formats You Can Use**
```json
// Hex colors (recommended)
"color": "#FF8A50"

// RGB arrays
"color": [255, 138, 80]

// RGBA arrays (for transparency)
"bg_color": [0, 0, 0, 180]
```

### 🔤 **Font Customization**
```json
"style": {
  "font_path": "fonts/montserrat-bold.ttf",  // Path to your font
  "font_size": 44,                           // Size in pixels
  "color": "#FF8A50"
}
```

### ✨ **Component Toggle Guide**

**Disable slide indicator:**
```json
"slide_indicator": {
  "enabled": false
}
```

**Remove X icon from myth statement:**
```json
"myth_statement": {
  "icon": {
    "draw_x_icon": false
  }
}
```

**Remove underline from "Truth:" label:**
```json
"truth_label": {
  "style": {
    "underline": false
  }
}
```

---

## 🧪 Step 5: Testing & Debugging

### 🔍 **Common Issues & Solutions**

**Issue: Font not found**
- **Solution**: Make sure font files are in the `fonts/` folder and paths are correct

**Issue: Text overlapping**
- **Solution**: Increase the `y_offset_percent_from_overlay_top` values

**Issue: Colors look wrong**
- **Solution**: Use hex colors (`#FF0000`) instead of RGB arrays for consistency

**Issue: Text too wide**
- **Solution**: Reduce `max_width_percent` (try 0.8 instead of 0.9)

### 🧪 **Quick Testing Template**

Create a simple test template `test_template.json`:

```json
{
  "canvas": {"width": 800, "height": 1000, "background_color": "#FFFFFF"},
  "image_area": {"height_percent": 0.5},
  "bottom_overlay": {
    "height_percent": 0.5,
    "gradient": {"from_rgba": [255,255,255,200], "to_rgba": [255,255,255,0]}
  },
  "slide_indicator": {"enabled": false},
  "myth_label": {
    "text": "Test Myth",
    "position": {"y_offset_percent_from_overlay_top": 0.1},
    "style": {"font_path": "fonts/arial.ttf", "font_size": 36, "color": "#FF0000"}
  },
  "myth_statement": {
    "text": "This is a test myth statement",
    "position": {"y_offset_percent_from_overlay_top": 0.25},
    "style": {"font_path": "fonts/arial.ttf", "font_size": 28, "color": "#FF0000"},
    "icon": {"draw_x_icon": false}
  },
  "truth_label": {
    "text": "Truth:",
    "position": {"y_offset_percent_from_overlay_top": 0.45},
    "style": {"font_path": "fonts/arial.ttf", "font_size": 24, "color": "#00FF00", "underline": true}
  },
  "truth_explanation": {
    "text": "This is the truth explanation that should wrap nicely across multiple lines.",
    "position": {"y_offset_percent_from_overlay_top": 0.6},
    "style": {"font_path": "fonts/arial.ttf", "font_size": 20, "color": "#000000", "max_width_percent": 0.8, "line_spacing": 6}
  },
  "margins": {"left_percent": 0.1, "right_percent": 0.1}
}
```

---

## 🚀 Step 6: Batch Generation Example

Create multiple posters at once:

```python
def batch_generate_myths():
    """Generate multiple myth posters"""
    myths = [
        {
            "myth": "Cracking knuckles causes arthritis",
            "truth": "No scientific evidence links knuckle cracking to arthritis. It's just gas bubbles in your joints!",
            "bg": "backgrounds/hands.jpg",
            "output": "knuckles-myth"
        },
        {
            "myth": "Reading in dim light damages eyes",
            "truth": "It causes temporary eye strain but no permanent damage. Your eyes will recover with rest.",
            "bg": "backgrounds/reading.jpg", 
            "output": "reading-myth"
        }
    ]
    
    for myth_data in myths:
        create_custom_poster(
            myth_text=myth_data["myth"],
            truth_text=myth_data["truth"],
            bg_image=myth_data["bg"],
            output_name=myth_data["output"]
        )

# Run batch generation
batch_generate_myths()
```

---

## 📱 Step 7: Platform-Specific Templates

### Instagram Post (1080x1350)
```json
"canvas": {"width": 1080, "height": 1350}
```

### Instagram Story (1080x1920)
```json
"canvas": {"width": 1080, "height": 1920},
"image_area": {"height_percent": 0.7},
"bottom_overlay": {"height_percent": 0.3}
```

### Twitter Post (1200x675)
```json
"canvas": {"width": 1200, "height": 675},
"image_area": {"height_percent": 0.6},
"bottom_overlay": {"height_percent": 0.4}
```

---

## 💡 Pro Tips

1. **Start Simple**: Begin with the test template before customizing
2. **Use Consistent Fonts**: Stick to 2-3 fonts max for professional look
3. **Color Psychology**: Red for myths (danger/warning), Green for truth (safety/correct)
4. **Mobile First**: 80% of social media is viewed on mobile, so ensure text is readable on small screens
5. **Batch Process**: Create templates for different content types (health, tech, finance myths)

---

## 🎉 You're Ready!

With this manual, you can now:

✅ Create professional-looking myth vs truth posters  
✅ Customize every aspect without touching the core code  
✅ Generate multiple posters quickly  
✅ Adapt templates for different social media platforms  
✅ Troubleshoot common issues  

**Next Steps:**
1. Set up your folder structure
2. Create your first template using the examples above
3. Run your first poster generation
4. Start customizing colors, fonts, and spacing

Happy poster creating! 🎨✨
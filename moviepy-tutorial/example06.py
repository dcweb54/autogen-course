import subprocess
import shlex
import os

def create_intro(
    text: str,
    logo_path: str,
    output_path: str = "intro.mp4",
    duration: int = 10,
    bg_color: str = "blue",
    font_path: str = "arial",
    text_effect: str = "bounce",
    logo_effect: str = "flyin",
):
    """
    Create a motion graphic intro using FFmpeg with customizable effects.

    text_effect:  "bounce", "slide", "fade"
    logo_effect:  "flyin", "fade", "slide"
    """

    # --- TEXT EFFECTS ---
    if text_effect == "bounce":
        text_anim = "x=w/2-tw/2:y=h-100+sin(t*2)*10"
    elif text_effect == "slide":
        text_anim = "x=w-t*200:y=h-150"
    elif text_effect == "fade":
        text_anim = f"x=w/2-tw/2:y=h-150:alpha='if(lt(t,1),0,if(lt(t,{duration - 2}),(t-1)/2,1))'"
    else:
        raise ValueError("Invalid text_effect")

    # --- LOGO EFFECTS ---
    if logo_effect == "flyin":
        logo_anim = "x=(W-w)/2:y=-h+200*t"
    elif logo_effect == "fade":
        logo_anim = "x=(W-w)/2:y=100:alpha='if(lt(t,2),0,if(lt(t,4),(t-2)/2,1))'"
    elif logo_effect == "slide":
        logo_anim = "x=-w+200*t:y=100"
    else:
        raise ValueError("Invalid logo_effect")

    # --- FFmpeg Command ---
    ffmpeg_cmd = f"""
    ffmpeg -y \
    -f lavfi -i "color={bg_color}:size=1280x720:duration={duration}" \
    -i "{logo_path}" \
    -filter_complex "
    [0:v]noise=alls=20:allf=t+u[bg]; \
    [bg]drawtext=fontfile={font_path}:text='{text}': \
         {text_anim}:fontsize=72:fontcolor=white:enable='between(t,1,{duration - 2})'[texted]; \
    [texted][1:v]overlay={logo_anim}:enable='between(t,2,{duration - 4})'[final]
    " \
    -map "[final]" -t {duration} -pix_fmt yuv420p -c:v libx264 "{output_path}"
    """

    subprocess.run(shlex.split(ffmpeg_cmd), check=True)
    print(
        f"✅ Intro video saved at {output_path} with text={text_effect}, logo={logo_effect}"
    )


if __name__ == "__main__":
    print("wewlcome")
    logo_png = os.path.join(os.path.join(os.getcwd(), "moviepy-learning-material"), "logo.png")
    current_output = os.path.join(os.path.join(os.getcwd(), "moviepy-learning-material-output", "intro_slide_fade.mp4"))

    create_intro(
        text="Hello World",
        logo_path=logo_png,
        output_path=current_output,
        text_effect="slide",
        logo_effect="fade",
    )

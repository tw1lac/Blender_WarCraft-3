from io_scene_warcraft_3.classes.WarCraft3Model import WarCraft3Model


def parse_model(data, model: WarCraft3Model):

    model.name = data.split(" ")[1].replace("\"", "")

    # model_info = extract_bracket_content(data).split(",")
    #
    # for info in model_info:
    #     label = info.strip().split(" ")[0]
    #     if label == "BlendTime":
    #         blendTime = int(info.strip().split(" ")[1])
    #     if label == "MinimumExtent":
    #         minimumExtent = info.strip().split(" ")[1]
    #     if label == "MaximumExtent":
    #         minimumExtent = info.strip().split(" ")[1]
    #     if label == "BoundsRadius":
    #         boundsRadius = info.strip().split(" ")[1]
    #     if label == "AnimationFileName":
    #         animationFileName = info.strip().split(" ")[1]

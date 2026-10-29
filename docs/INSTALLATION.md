# Installation and First Run

**Built by I2PS Engineering · LogicaSophia 0.7.0 · Ubuntu Linux x86-64**

## Obtain the actual application

The public GitHub repository is a **product/documentation repository**, not a public source distribution. Obtain the **I2PS-issued** archive `LogicaSophia_0.7.0_Private_Engineering_Studio.zip` separately. This README does not claim that the ZIP is already attached to a GitHub Release.

Package SHA-256:
`b9ef54e36d9f3ecc569d5be66978955fcbf8d24e9986351db93b596d1e8f62cf`

Verify it:
~~~bash
sha256sum LogicaSophia_0.7.0_Private_Engineering_Studio.zip
~~~

Extract, then enter the extracted `LogicaSophia_0.7.0_Private_Engineering_Studio` directory.

## Start with native analysis (without a foundation model)

~~~bash
bash LogicaSophia_Start_AI.txt native
~~~

This starts the localhost browser console using the native deterministic analyzer. A trained language model is not required for the supported limited file/AST tasks.

## Install the optional Qt desktop and voice stack

On Ubuntu x86-64, with internet available:
~~~bash
bash LogicaSophia_Setup_Lexia_And_Studio.txt
bash LogicaSophia_Start_AI.txt qt
~~~

The setup installs PySide6, Pillow, ReportLab, NumPy, SoundFile and the pinned `kokoro-onnx==0.6.1` dependency into the package folder. It retrieves Kokoro model resources with mandatory SHA-256 checks. Some Ubuntu configurations need system voice shared libraries such as `libespeak-ng1` and `libsndfile1`. First download may require several hundred MB. The intended initial test host has ~7.1 GiB RAM, a four-thread i5 and no discrete GPU; this is test context, **not a universal minimum specification**.

## Create an engineering chart and PDF from CSV

The package includes sample `workspace/measurements.csv` data:
~~~bash
bash LogicaSophia_Start_AI.txt work --goal 'Create chart and report from measurements.csv'
~~~
This displays the proposed plan. To execute after review:
~~~bash
bash LogicaSophia_Start_AI.txt work --goal 'Create chart and report from measurements.csv' --confirm
~~~

The generated results and hash manifest are written outside the input workspace, under the per-user results directory. The included sample is not field telemetry.

## Speech and narration

Run the Kokoro setup first. Narration scripts use `SLIDE NN — TITLE` headings. Lexia's process requires audit, short real clip, review of unknown pronunciations, human approval and then full render. The full approved settings are in [Lexia Voice](VOICE_LEXIA.md).

Do not treat an unapproved pronunciation or the existence of a script as permission for automated voice rendering.

## Text-to-image with authentic logo

Install and start a compatible local ComfyUI server separately. Select an actual installed image checkpoint. For a corporate emblem on a generated subject, supply the authentic I2PS logo asset and inspect its placement. The approved LogicaSophia identity JPEG is a **different asset** from the I2PS company logo and must not be silently substituted. The program must return a missing-dependency error if the checkpoint or logo is absent.

## Optional external foundation model

External local inference can be selected explicitly using the launcher or UI. It is not mandatory and no model vendor is prescribed. The native controller remains the I2PS-controlled policy and evidence layer.

## Verification

The package was integrity-checked locally. Qt desktop visual interactions, ComfyUI generation and real Kokoro narration still need qualification on a target Linux host. Never infer them from a successful install.

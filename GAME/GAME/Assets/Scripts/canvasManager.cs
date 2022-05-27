using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class canvasManager : MonoBehaviour
{

    public GlobalVolumeManager volumeManager;
    public CanvasGroup BlackRedCanvasGroup;
    public CanvasGroup BlackBlueCanvasGroup;
    public CanvasGroup LevelText1;
    public CanvasGroup LevelText2;
    public CanvasGroup LevelText3;
    public CanvasGroup LevelText4;
    public CanvasGroup LevelText5;
    public CanvasGroup Pause; 
    bool enMenu;
    bool enPausa;
    bool enCredits;


    // Start is called before the first frame update
    void Start()
    {
        enMenu = false; 
        enPausa = false;
        enCredits = false;
        LevelText1.alpha = 0f; LevelText2.alpha = 0f; LevelText3.alpha = 0f; LevelText4.alpha = 0f; LevelText5.alpha = 0f; BlackBlueCanvasGroup.alpha = 0f; BlackRedCanvasGroup.alpha = 0f; Pause.alpha = 0f;
        //volumeManager.clearBlur();
    }

    // Update is called once per frame
    void Update()
    {
        if (!enMenu && !enCredits)
        {
            if (Input.GetKeyDown(KeyCode.Escape))
            {
                if (!enPausa)
                {
                    enPausa = true;
                    Time.timeScale = 0;
                    volumeManager.setBlur();
                    Pause.alpha = 1.0f;
                }
                else
                {
                    enPausa = false;
                    Time.timeScale = 1;
                    volumeManager.clearBlur();
                    Pause.alpha = 0f;
                }
            }
        }
    }



    public IEnumerator transitionRedExposureNegre(float duration)
    {
        float currentTemps = 0.0f;

        while (true)
        {
            currentTemps += Time.deltaTime;
            if (currentTemps < (duration / 2.0f))
            { //fem menys exposicio
                BlackRedCanvasGroup.alpha = (currentTemps / (duration / 2.0f)) * 3f;
                yield return null;
            }
            else
            { //tornem la expo a com estava
                BlackRedCanvasGroup.alpha = 3.0f - ((currentTemps - (duration / 2.0f)) / (duration / 2.0f)) * 3f;
                yield return null;
            }

            Debug.Log(BlackRedCanvasGroup.alpha);

            if (currentTemps > duration)
            {
                BlackRedCanvasGroup.alpha = 0f;
                break;
            }
        }

        yield return null;
    }


    public IEnumerator transitionBlueExposureNegre(float duration)
    {
        float currentTemps = 0.0f;

        while (true)
        {
            currentTemps += Time.deltaTime;
            if (currentTemps < (duration / 2.0f))
            { //fem menys exposicio
                BlackBlueCanvasGroup.alpha = (currentTemps / (duration / 2.0f)) * 3f;
                yield return null;
            }
            else
            { //tornem la expo a com estava
                BlackBlueCanvasGroup.alpha = 3.0f - ((currentTemps - (duration / 2.0f)) / (duration / 2.0f)) * 3f;
                yield return null;
            }

            Debug.Log(BlackBlueCanvasGroup.alpha);

            if (currentTemps > duration)
            {
                BlackBlueCanvasGroup.alpha = 0f;
                break;
            }
        }

        yield return null;
    }

    public void activaCanviaLevelText(int level)
    {
        LevelText1.alpha = 0f; LevelText2.alpha = 0f; LevelText3.alpha = 0f; LevelText4.alpha = 0f; LevelText5.alpha = 0f;

        if (!enMenu && !enPausa && !enCredits)
        {
            if (level == 1)
            {
                LevelText1.alpha = 1f;
            }
            else if (level == 2)
            {
                LevelText2.alpha = 1f;
            }
            else if (level == 3)
            {
                LevelText3.alpha = 1f;
            }
            else if (level == 4)
            {
                LevelText4.alpha = 1f;
            }
            else if (level == 5)
            {
                LevelText5.alpha = 1f;
            }

        }
    }

    public void continuePausa()
    {
        enPausa = false;
        Time.timeScale = 1;
        volumeManager.clearBlur();
        Pause.alpha = 0f;
    }

}

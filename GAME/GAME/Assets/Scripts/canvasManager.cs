using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class canvasManager : MonoBehaviour
{

    public GlobalVolumeManager volumeManager;
    public Camera cameraMenu;
    public Camera CreditsCamera;
    public CanvasGroup BlackRedCanvasGroup;
    public CanvasGroup BlackBlueCanvasGroup;
    public CanvasGroup LevelText1;
    public CanvasGroup LevelText2;
    public CanvasGroup LevelText3;
    public CanvasGroup LevelText4;
    public CanvasGroup LevelText5;
    public Canvas Pause;
    public Canvas Credits;
    public Canvas Menu;
    public RedPlayerMovement redplayer;
    public BluePlayerMovement blueplayer; 
    bool enMenu;
    bool enPausa;
    bool enCredits;
    public AudioSource playMusic;
    public AudioSource MenuMusic;
    public AudioSource soundSelected; 


    // Start is called before the first frame update
    void Start()
    {
        enMenu = true;
        CreditsCamera.enabled = false;
        enPausa = false;
        enCredits = false;
        LevelText1.alpha = 0f; LevelText2.alpha = 0f; LevelText3.alpha = 0f; LevelText4.alpha = 0f; LevelText5.alpha = 0f; BlackBlueCanvasGroup.alpha = 0f; BlackRedCanvasGroup.alpha = 0f; Pause.enabled = false; Credits.enabled = false; 
        Menu.enabled = true;
        Time.timeScale = 1;
        volumeManager.clearBlur();
        //redplayer.ComensaPrincipi();
        //blueplayer.ComensaPrincipi();
        cameraMenu.enabled = true;
        MenuMusic.Play();
        playMusic.Stop();
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
                    soundSelected.Play();
                    playMusic.Pause();
                    enPausa = true;
                    Time.timeScale = 0;
                    volumeManager.setBlur();
                    Pause.enabled = true;
                    soundSelected.Play(); 
                }
                else
                {
                    soundSelected.Play(); 
                    playMusic.UnPause(); 
                    enPausa = false;
                    Time.timeScale = 1;
                    volumeManager.clearBlur();
                    Pause.enabled = false;
                    soundSelected.Play(); 
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
        playMusic.UnPause();
        enPausa = false;
        Time.timeScale = 1;
        volumeManager.clearBlur();
        Pause.enabled = false;
        soundSelected.Play(); 
    }

    public void MenuPausa()
    {   playMusic.Stop();
        MenuMusic.UnPause(); 
        Time.timeScale = 1;
        enPausa = false;
        volumeManager.clearBlur();
        redplayer.ComensaPrincipi(); 
        blueplayer.ComensaPrincipi();
        Pause.enabled = false;
        Menu.enabled = true;
        cameraMenu.enabled = true;
        soundSelected.Play(); 

    }

    public void PlayMenu()
    {
        playMusic.Play(); 
        MenuMusic.Pause();
        volumeManager.clearBlur();
        enMenu = false;
        Menu.enabled = false; 
        cameraMenu.enabled = false;
        redplayer.ComensaPrincipi();
        blueplayer.ComensaPrincipi();
        soundSelected.Play();
    }

    public void ExitMenu()
    {
        Application.Quit(); 
    }

    public void CreditsMenu()
    {
        volumeManager.setBlur();
        enMenu = false;
        enCredits = true;
        Menu.enabled = false;
        cameraMenu.enabled = false;
        Credits.enabled = true;
        CreditsCamera.enabled = true;
        soundSelected.Play(); 
    }

    public void ExitCredits()
    {
        volumeManager.clearBlur();
        enMenu = true;
        enCredits = false; 
        Menu.enabled=true;
        cameraMenu.enabled = true;
        Credits.enabled = false;
        CreditsCamera.enabled = false;
        soundSelected.Play(); 
    }    

}

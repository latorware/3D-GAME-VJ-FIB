using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class canvasManager : MonoBehaviour
{


    public CanvasGroup BlackRedCanvasGroup;
    public CanvasGroup BlackBlueCanvasGroup;


    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {

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

}

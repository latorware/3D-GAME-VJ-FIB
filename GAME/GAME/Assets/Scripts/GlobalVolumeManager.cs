using System.Collections;
using System.Collections.Generic;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;
using UnityEngine;

public class GlobalVolumeManager : MonoBehaviour
{

    private ColorAdjustments ColorAdjustment;



    // Start is called before the first frame update
    void Start()
    {
        Volume volume = GetComponent<Volume>();

        volume.sharedProfile.TryGet<ColorAdjustments>(out ColorAdjustment);

        ColorAdjustment.postExposure.value = 0f;
    }

    // Update is called once per frame
    void Update()
    {

    }

    /*
    public IEnumerator transitionExposureNegre(float duration)
    {
        float currentTemps = 0.0f;
        
        while (true)
        {
            currentTemps += Time.deltaTime;
            if (currentTemps < (duration / 2.0f))
            { //fem menys exposicio
                ColorAdjustment.postExposure.value = (currentTemps / (duration / 2.0f)) * (-8.0f);
                yield return null;
            }
            else
            { //tornem la expo a com estava
                ColorAdjustment.postExposure.value = (1.0f-((currentTemps - (duration / 2.0f)) / (duration / 2.0f))) * (-8.0f);
                yield return null; 
            }



            if (currentTemps > duration)
            {
                ColorAdjustment.postExposure.value = 0f; break;
            }
        }

        yield return null; 
    }
    */


    public IEnumerator transitionExposureBlanc(float duration)
    {
        float currentTemps = 0.0f;

        while (true)
        {
            currentTemps += Time.deltaTime;
            if (currentTemps < (duration / 2.0f))
            { //fem menys exposicio
                ColorAdjustment.postExposure.value = (currentTemps / (duration / 2.0f)) * (8.0f);
                yield return null;
            }
            else
            { //tornem la expo a com estava
                ColorAdjustment.postExposure.value = (1.0f - ((currentTemps - (duration / 2.0f)) / (duration / 2.0f))) * (8.0f);
                yield return null;
            }



            if (currentTemps > duration)
            {
                ColorAdjustment.postExposure.value = 0f; break;
            }
        }

        yield return null;
    }

    public void BlancINegre()
    {
        ColorAdjustment.saturation.value = -100f;
    }

    public void Color()
    {
        ColorAdjustment.saturation.value = 25f;
    }
}

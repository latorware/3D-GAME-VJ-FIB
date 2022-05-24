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
    }

    // Update is called once per frame
    void Update()
    {

    }


    public void transitionExposure(float duration)
    {
        return; 
    }
}

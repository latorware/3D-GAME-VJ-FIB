using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CreateInvaders : MonoBehaviour
{
    public GameObject invader;

    // Start is called before the first frame update
    void Start()
    {
        GameObject obj;

        for (int j = 0; j < 4; j++)
            for (int i = 0; i < 8; i++)
            {
                obj = (GameObject)Instantiate(invader, new Vector3(1.5f * i - 5.25f, j + 1.0f, 0.0f), transform.rotation);
                obj.transform.parent = transform;
            }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Shoot : MonoBehaviour
{
    public float speed = 20.0f;
    public GameObject shot;

    public AudioClip shootSound;

    float timeToNextShot = 0.0f;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        timeToNextShot -= Time.deltaTime;
        if(Input.GetKey(KeyCode.Space) && timeToNextShot <= 0.0f)
        {
            timeToNextShot = 0.5f;
            GameObject obj = Instantiate(shot, transform.position + new Vector3(0.0f, 1.0f, 0.0f), transform.rotation);
            obj.GetComponent<Rigidbody>().velocity = new Vector3(0.0f, speed, 0.0f);

            AudioSource.PlayClipAtPoint(shootSound, transform.position);
        }
    }
}

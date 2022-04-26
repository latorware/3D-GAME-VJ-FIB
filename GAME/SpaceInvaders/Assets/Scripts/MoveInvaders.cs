using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MoveInvaders : MonoBehaviour
{
    public float speed = 3.0f;

    float direction = 1.0f;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        transform.Translate(direction * speed * Time.deltaTime, 0.0f, 0.0f);
        if (direction > 0.0f && transform.position.x >= 4.0f)
        {
            direction = -1.0f;
            transform.Translate(0.0f, -1.0f, 0.0f);
        }
        if (direction < 0.0f && transform.position.x <= -4.0f)
        {
            direction = 1.0f;
            transform.Translate(0.0f, -1.0f, 0.0f);
        }
    }
}

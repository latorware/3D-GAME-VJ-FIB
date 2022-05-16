using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RedPlayerMovement : MonoBehaviour
{

    public float speed;
    private CharacterController characterController; 
    private Animator animator;
    private Rigidbody myRigidbody;
    public float FallingThreshold = -10f;
    [HideInInspector]
    public bool Falling = false;


    // Start is called before the first frame update
    void Start()
    {
        animator = GetComponent<Animator>();
        characterController = GetComponent<CharacterController>();
        myRigidbody = GetComponent<Rigidbody>();
        characterController.Move(new Vector3(0f, 0f, .01f) * speed * Time.deltaTime);
        //myRigidbody.velocity = new Vector3(0f, 100f, 0f); 
    }

    // Update is called once per frame
    void Update()
    {

        if (myRigidbody.velocity.y < FallingThreshold)
        {
            Falling = true;
            animator.SetBool("isMoving", false);
        }
        else
        {
            Falling = false;
        }

        if (!Falling)
        {
            bool input = Input.GetKey(KeyCode.W);

            if (input)
            {
                Vector3 movementDirection = new Vector3(0f, 0f, 1f);
                float magnitude = Mathf.Clamp01(movementDirection.magnitude) * speed; 
                movementDirection.Normalize();
                characterController.SimpleMove(movementDirection * magnitude);
                animator.SetBool("isMoving", true);
            }
            else
            {
                animator.SetBool("isMoving", false);
            }

        }

    }
}

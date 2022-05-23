using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using PathCreation; 

public class RedPlayerMovement : MonoBehaviour
{

    public float speed;
    //private CharacterController characterController; 
    private Animator animator;
    private Rigidbody myRigidbody;
    public float FallingThreshold = -10f;
    private Transform myTransform;
    public PathCreator pathCreator; 
    public float forceGrupPunxes1;
    public float forceGrupPunxes2;
    public float forceGrupPunxes3;
    public float forceGirador1; 
    public float forceGirador2;
    [HideInInspector]
    private bool Falling; 
    float pathState;
    bool colisionat; 


    // Start is called before the first frame update
    void Start()
    {
        Falling = false; 
        colisionat = false;
        animator = GetComponent<Animator>();
        //characterController = GetComponent<CharacterController>();
        myRigidbody = GetComponent<Rigidbody>();
        //characterController.Move(new Vector3(0f, 0f, .01f) * speed * Time.deltaTime);
        //myRigidbody.velocity = new Vector3(0f, 100f, 0f);
        myTransform = GetComponent<Transform>();

        myRigidbody.sleepThreshold = 0.0f;

    }

    private void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.name == "punxes1" || collision.gameObject.name == "punxes2" || collision.gameObject.name == "punxes3" || collision.gameObject.name == "punxes4")
        {
            //myRigidbody.AddForce(new Vector3(collision.contacts[0].normal.x, collision.contacts[0].normal.y, collision.contacts[0].normal.z) * forceGrupPunxes1);
            myRigidbody.AddForce(new Vector3(-1f, 1f, -1f) * forceGrupPunxes1);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }
        else if (collision.gameObject.name == "punxes8")
        {
            myRigidbody.AddForce(new Vector3(0f, 1f, 1f) * forceGrupPunxes2);
            colisionat=true;
            animator.SetBool("isMoving", false);
        }
        else if (collision.gameObject.name == "punxes11")
        {
            myRigidbody.AddForce(new Vector3(-1f, 1f, 0f) * forceGrupPunxes3);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }
        else if (collision.gameObject.name == "cGran1")
        {
            myRigidbody.AddForce(collision.contacts[0].normal * forceGirador1);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }
        else if (collision.gameObject.name == "cGran2")
        {
            myRigidbody.AddForce(collision.contacts[0].normal * forceGirador2);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }

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

        if (!Falling && !colisionat)
        {
            if (Input.GetKey(KeyCode.W))
            {
                pathState += speed * Time.deltaTime;
                Vector3 pathPosition = pathCreator.path.GetPointAtDistance(pathState);
                Vector3 pathPositionNext = pathCreator.path.GetPointAtDistance(pathState * 1.01f);
                myTransform.position = new Vector3((float)pathPosition.x, myTransform.position.y, (float)pathPosition.z);
                //myTransform.rotation = pathCreator.path.GetRotationAtDistance(pathState); 
                transform.LookAt(new Vector3((float)pathPositionNext.x, myTransform.position.y, (float)pathPositionNext.z));
                animator.SetBool("isMoving", true);
            }
            else
            {
                animator.SetBool("isMoving", false);
            }
        }


        else if (colisionat)
        { //reseteja 
        }







    }
}

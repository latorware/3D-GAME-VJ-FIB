using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using PathCreation; 

public class RedPlayerMovement : MonoBehaviour
{

    public float speed;
    private Animator animator;
    private Rigidbody myRigidbody;
    public float FallingThreshold = -10f;
    private int currentNivell;
    private Transform myTransform;

    public GlobalVolumeManager volumeManager;


    public PathCreator pathCreator1;
    public PathCreator pathCreator2;
    public PathCreator pathCreator3;
    public PathCreator pathCreator4;
    public PathCreator pathCreator5;

    //Nivell 2
    public float forceGrupPunxes1;
    public float forceGrupPunxes2;
    public float forceGrupPunxes3;
    public float forceGirador1; 
    public float forceGirador2;

    //Nivell 1
    public float forceTorusNivell1;
    public float forced; 



    [HideInInspector]
    private bool Falling; 
    float pathState;
    bool colisionat;
    bool fentRestart;
    bool canviantNivell; 


    // Start is called before the first frame update
    void Start()
    {
        animator = GetComponent<Animator>();
        myRigidbody = GetComponent<Rigidbody>();
        myTransform = GetComponent<Transform>();
        myRigidbody.sleepThreshold = 0.0f;
        canviantNivell = false;
        ComensaNivell(1); 

    }

    private void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.name == "punxes1" || collision.gameObject.name == "punxes2" || collision.gameObject.name == "punxes3" || collision.gameObject.name == "punxes4")
        {
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
        else if (collision.gameObject.name == "Torus1" || collision.gameObject.name == "Torus2")
        {
            myRigidbody.AddForce(collision.contacts[0].normal * forceTorusNivell1);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }
        else if (collision.gameObject.name == "d2" || collision.gameObject.name == "d1" || collision.gameObject.name == "d3")
        {
            myRigidbody.AddForce(collision.contacts[0].normal * forced);
            colisionat = true;
            animator.SetBool("isMoving", false);
        }

    }


    // Update is called once per frame
    void Update()
    {

        if (!canviantNivell)
        {
            if ((Input.GetKey(KeyCode.Alpha1)) && (currentNivell != 1))
            {
                canviantNivell = true;
                animator.SetBool("isMoving", false);
                StartCoroutine(canviaNivell(1)); 
            }
            else if ((Input.GetKey(KeyCode.Alpha2)) && (currentNivell != 2))
            {
                canviantNivell = true;
                animator.SetBool("isMoving", false);
                StartCoroutine(canviaNivell(2));
            }
            else if ((Input.GetKey(KeyCode.Alpha3)) && (currentNivell != 3))
            {
                canviantNivell = true;
                animator.SetBool("isMoving", false);
                StartCoroutine(canviaNivell(3));
            }
            else if ((Input.GetKey(KeyCode.Alpha4)) && (currentNivell != 4))
            {
                canviantNivell = true;
                animator.SetBool("isMoving", false);
                StartCoroutine(canviaNivell(4));
            }
            else if ((Input.GetKey(KeyCode.Alpha5)) && (currentNivell != 5))
            {
                canviantNivell = true;
                animator.SetBool("isMoving", false);
                StartCoroutine(canviaNivell(5));
            }
            else
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

                if (!Falling && !colisionat && !fentRestart)
                {
                    if (Input.GetKey(KeyCode.W))
                    {
                        if (currentNivell == 1)
                        {
                            MouNivell1();
                        }
                        else if (currentNivell == 2)
                        {
                            MouNivell2();
                        }
                        else if (currentNivell == 3)
                        {
                            MouNivell3();
                        }
                        else if (currentNivell == 4)
                        {
                            MouNivell4();
                        }
                        else if (currentNivell == 5)
                        {
                            MouNivell5();
                        }
                    }
                    else
                    {
                        animator.SetBool("isMoving", false);
                    }
                }


                else if (colisionat && !fentRestart)
                { //reseteja 
                    fentRestart = true;
                    StartCoroutine(restartNivell());
                }
            }

        }



    }



    private void ComensaNivell(int nivell)
    {
        myRigidbody.useGravity = true;
        Falling = false;
        colisionat = false;
        currentNivell = nivell;
        //posicio i mirar en principi nivell
        pathState = 0f;
        if (nivell == 1)
        {
            Vector3 pathPosition = pathCreator1.path.GetPointAtDistance(pathState);
            myTransform.position = new Vector3((float)pathPosition.x, (float)pathPosition.y, (float)pathPosition.z);
            transform.LookAt(new Vector3(5000f, 0f, 0f)); 
        }
        else if (nivell == 2)
        {
            Vector3 pathPosition = pathCreator2.path.GetPointAtDistance(pathState);
            myTransform.position = new Vector3((float)pathPosition.x, (float)pathPosition.y, (float)pathPosition.z);
            transform.LookAt(new Vector3(0f, 0f, 5000f));
        }
        else if (nivell == 3)
        {
            Vector3 pathPosition = pathCreator3.path.GetPointAtDistance(pathState);
            myTransform.position = new Vector3((float)pathPosition.x, (float)pathPosition.y, (float)pathPosition.z);
            transform.LookAt(new Vector3(0f, 0f, 5000f));
        }
        else if (nivell == 4)
        {
            Vector3 pathPosition = pathCreator4.path.GetPointAtDistance(pathState);
            myTransform.position = new Vector3((float)pathPosition.x, (float)pathPosition.y, (float)pathPosition.z);
            transform.LookAt(new Vector3(0f, 0f, -5000f));
        }
        else if (nivell == 5)
        {
            Vector3 pathPosition = pathCreator5.path.GetPointAtDistance(pathState);
            myTransform.position = new Vector3((float)pathPosition.x, (float)pathPosition.y, (float)pathPosition.z);
            transform.LookAt(new Vector3(5000f , 0f, 0f));
        }
    }

    private void MouNivell1()
    {
        pathState += speed * Time.deltaTime;
        Vector3 pathPosition = pathCreator1.path.GetPointAtDistance(pathState);
        Vector3 pathPositionNext = pathCreator1.path.GetPointAtDistance(pathState * 1.01f);
        myTransform.position = new Vector3((float)pathPosition.x, myTransform.position.y, (float)pathPosition.z);
        transform.LookAt(new Vector3((float)pathPositionNext.x, myTransform.position.y, (float)pathPositionNext.z));
        animator.SetBool("isMoving", true);
    }

    private void MouNivell2()
    {
        pathState += speed * Time.deltaTime;
        Vector3 pathPosition = pathCreator2.path.GetPointAtDistance(pathState);
        Vector3 pathPositionNext = pathCreator2.path.GetPointAtDistance(pathState * 1.01f);
        myTransform.position = new Vector3((float)pathPosition.x, myTransform.position.y, (float)pathPosition.z);
        transform.LookAt(new Vector3((float)pathPositionNext.x, myTransform.position.y, (float)pathPositionNext.z));
        animator.SetBool("isMoving", true);
    }

    private void MouNivell3()
    {
        pathState += speed * Time.deltaTime;
        Vector3 pathPosition = pathCreator3.path.GetPointAtDistance(pathState);
        Vector3 pathPositionNext = pathCreator3.path.GetPointAtDistance(pathState * 1.01f);
        myTransform.position = new Vector3((float)pathPosition.x, myTransform.position.y, (float)pathPosition.z);
        transform.LookAt(new Vector3((float)pathPositionNext.x, myTransform.position.y, (float)pathPositionNext.z));
        animator.SetBool("isMoving", true);
    }

    private void MouNivell4()
    {
        pathState += speed * Time.deltaTime;
        Vector3 pathPosition = pathCreator4.path.GetPointAtDistance(pathState);
        Vector3 pathPositionNext = pathCreator4.path.GetPointAtDistance(pathState * 1.01f);
        if (pathState > 286.0f)
        {
            myRigidbody.useGravity = false; 
            myTransform.position = new Vector3((float)pathPosition.x, (float)pathPosition.y, (float)pathPosition.z);
            //transform.LookAt(new Vector3((float)pathPositionNext.x, (float)pathPosition.y, (float)pathPositionNext.z));
            animator.SetBool("isMoving", true);
        }
        else
        {
            myTransform.position = new Vector3((float)pathPosition.x, myTransform.position.y, (float)pathPosition.z);
            transform.LookAt(new Vector3((float)pathPositionNext.x, myTransform.position.y, (float)pathPositionNext.z));
            animator.SetBool("isMoving", true);
        }
    }

    private void MouNivell5()
    {
        pathState += speed * Time.deltaTime;
        Vector3 pathPosition = pathCreator5.path.GetPointAtDistance(pathState);
        Vector3 pathPositionNext = pathCreator5.path.GetPointAtDistance(pathState * 1.01f);
        myTransform.position = new Vector3((float)pathPosition.x, myTransform.position.y, (float)pathPosition.z);
        transform.LookAt(new Vector3((float)pathPositionNext.x, myTransform.position.y, (float)pathPositionNext.z));
        animator.SetBool("isMoving", true);
    }

    
    private IEnumerator restartNivell()
    {
        yield return new WaitForSeconds(2f);
        StartCoroutine(volumeManager.transitionExposureNegre(2f));
        yield return new WaitForSeconds(1f);
        myRigidbody.velocity = Vector3.zero;
        ComensaNivell(currentNivell);
        yield return new WaitForSeconds(1f);
        fentRestart = false; 
        yield return null; 
    }

    private IEnumerator canviaNivell(int nivell)
    {
        //yield return new WaitForSeconds(2f);
        StartCoroutine(volumeManager.transitionExposureBlanc(2f));
        yield return new WaitForSeconds(1f);
        myRigidbody.velocity = Vector3.zero;
        ComensaNivell(nivell);
        yield return new WaitForSeconds(1f);
        canviantNivell = false; 
        yield return null;
    }


    /*
    private IEnumerator TransicioNivell(int anterior, int següent)
    {
        
    }
    */

}
